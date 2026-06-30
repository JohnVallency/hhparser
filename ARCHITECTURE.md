# Архитектура проекта HH Parser

## 1. Сбор данных (Scrapy Spider)

**Файл:** `hhparser/spiders/hhparser.py`

### Процесс парсинга

1. **Стартовая страница** — `https://hh.ru/employers_list?areaId=1&vacanciesRequired=true`
2. **Пагинация каталога** — каталог компаний состоит из 50 страниц, так что парсер проходится с первой по 50 страницу при помощи форматирования номера страницы в ссылке.
3. **Для каждой компании:**
   - Извлекается название и ID компании
   - Формируется URL поиска вакансий: `https://hh.ru/search/vacancy?employer_id={id}`
   - Отправляется запрос в `parse_employer`
4. **На странице вакансий:**
   - Парсятся карточки вакансий через CSS-селекторы
   - Извлекаются: название, зарплата, локация, ссылка

### Защита от блокировок

В `settings.py` настроены параметры для предотвращения блокировки со стороны hh.ru:

```python
CONCURRENT_REQUESTS = 16 # максимум 16 параллельных запросов
CONCURRENT_REQUESTS_PER_DOMAIN = 8 # 8 параллельных запросов к hh.ru
DOWNLOAD_DELAY = 0.5 # задержка в 0.5 секунд предотвращает ошибку 429
```
## 2. Нормализация данных
Текст с зарплатой приходит со спецсимволами Unicode: \
`'70\u202f000 – 90\u202f000 ₽ \xa0 за\xa0месяц,  на руки'`
Зарплата очищается через цепочку замен:\
```python
salary_parts = card.css('span[class*="magritte-text_typography-label-1-regular"]::text').getall()
salary = ' '.join(salary_parts).replace('\u202f', '').replace('\xa0', ' ').strip()
```
Остальные данные достаются в нормальном виде и напрямую экспортируются.\
Для защиты от дубликатов в таблице companies поле name имеет constraint UNIQUE, а так же Метод save_company() использует INSERT OR IGNORE.

## 3. Сохранение данных (SQLite)
Файл: `hh_db.py` \
Структура базы данных:

<img width="965" height="408" alt="BD_SCHEME" src="https://github.com/user-attachments/assets/5bf66061-d490-4851-9506-ab6040a19835" />

SQLite — встроенная БД, не требует установки сервера \
check_same_thread=False — разрешает использовать соединение из разных потоков (нужно для FastAPI) \
CURRENT_TIMESTAMP — время сохраняется в UTC

## 4. Предоставление данных
### REST API (FastAPI)
FastAPI сервер предоставляет endpoints для чтения данных из БД:

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/` | GET | Главная страница |
| `/companies` | GET | Список всех компаний |
| `/companies/{id}` | GET | Компания по ID |
| `/vacancies` | GET | Список всех вакансий |
| `/vacancies/{id}` | GET | Вакансия по ID |
| `/vacancies/by-company/{company_id}` | GET | Вакансии компании |

**Особенности:**
- Автоматическая документация Swagger на `/docs`
- Асинхронная обработка запросов через uvicorn
- HTTP-коды ошибок (404 при отсутствии записи)

### Экспорт в Excel (pandas)

**Файл:** `export_excel.py`

Скрипт формирует файл `top_companies.xlsx` с двумя листами:

1. **Топ-20 компаний** — отсортированных по количеству вакансий
2. **Вакансии топ-20** — все вакансии этих компаний

**Алгоритм:**
1. Загружаются все компании из БД
2. Из текста `vacancies_count` регулярным выражением извлекается число
3. Компании сортируются по этому числу, берутся топ-20
4. Для этих компаний загружаются все вакансии
5. Данные сохраняются в Excel через `pandas` + `openpyxl`

## 5. Главный скрипт запуска

**Файл:** `hhparser_cls.py`

Объединяет все этапы в один процесс:

1. Установку зависимостей
2. Парсинг
3. Запуск API

## 6. Структура проекта

```
hhparser/
├── hhparser_cls.py          # Главный скрипт запуска
├── api.py                   # FastAPI сервер
├── hh_db.py                 # Модуль работы с SQLite
├── export_excel.py          # Экспорт в Excel
├── requirements.txt         # Зависимости Python
├── scrapy.cfg              # Конфигурация Scrapy
├── README.md               # Документация
├── ARCHITECTURE.md         # Этот файл
├── hhparser.db             # База данных (создаётся автоматически)
├── hh.csv                  # CSV-экспорт вакансий
├── top_companies.xlsx      # Excel-отчёт (создаётся export_excel.py)
│
└── hhparser/               # Пакет Scrapy
    ├── __init__.py
    ├── settings.py         # Настройки Scrapy
    ├── items.py            # Модели данных (не используются)
    ├── middlewares.py      # Middleware (не используются)
    ├── pipelines.py        # Pipelines (не используются)
    └── spiders/
        ├── __init__.py
        └── hhparser.py     # Основной парсер
```
