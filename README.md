# Парсер вакансий и компаний с сайта hh.ru
Автоматизированный парсер для сбора данных о вакансиях и компаниях с сайта hh.ru с последующим сохранением в базу данных, предоставлением REST API и экспортом в Excel.

## Быстрая установка
1. Склонировать репозиторий
2. Запустить скрипт `python hhparser_cls.py` , он сам установит зависимости, запустит парсинг и API.

## Ручная установка
1. Клонируйте репозиторий
2. Установите зависимости `pip install -r requirements.txt`
3. Запустите скрипт для парсинга `scrapy crawl hhparser`
4. Запустите API `python -m uvicorn api:app --host 127.0.0.1 --port 8000`
5. (Опционально) Экспортируйте топ-20 компаний в Excel `python export_excel.py`

## Тестовые данные
В репозитории так же сохранены тестовые данные [test_hhparser.db](test_hhparser.db) и [test_top_companies.xlsx](test_top_companies.xlsx) \
_Данные актуальны на 30.06.2026_

## Настройка
Подробная настройка описана в документации [Scrapy](https://docs.scrapy.org)

## Решение проблем
- Ошибка 429 (Too Many Requests) - Увеличьте `DOWNLOAD_DELAY`(время задержки) в `settings.py`

## Возможности
- Экспорт в различные форматы (JSON, CSV, JSON Lines, XML)
- Сохранение в базу данных SQLite
- Доступ через HTTP-запросы (REST API)
- Настройка скриптов

## Используемые инструменты
- Python 3.x - основной язык программирования проекта
- [Scrapy](https://scrapy.org) - фреймворк для веб-скрейпинга и парсинга сайтов, используется для сбора данных с hh.ru
- [SQLite](https://sqlite.org) - встроенная реляционная база данных для хранения компаний и вакансий
- [FastAPI](https://fastapi.tiangolo.com) - современный веб-фреймворк для создания REST API с автоматической документацией
- [pandas](https://pandas.pydata.org) - библиотека для анализа и обработки данных, используется для экспорта в Excel
- [openpyxl](https://openpyxl.readthedocs.io/en/stable) - библиотека для работы с Excel файлами (.xlsx)
- [uvicorn](https://uvicorn.dev) - ASGI сервер для запуска FastAPI приложений

## API Endpoints

После запуска API доступен по адресу: `http://127.0.0.1:8000`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/` | Главная страница |
| GET | `/companies` | Список всех компаний |
| GET | `/companies/{id}` | Компания по ID |
| GET | `/vacancies` | Список всех вакансий |
| GET | `/vacancies/{id}` | Вакансия по ID |
| GET | `/vacancies/by-company/{company_id}` | Вакансии компании |

**Документация Swagger:** http://127.0.0.1:8000/docs

## Структура базы данных

### Таблица `companies`
| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER | Уникальный идентификатор |
| name | TEXT | Название компании |
| vacancies_count | TEXT | Количество вакансий |
| created_at | TIMESTAMP | Дата добавления |
### Таблица `vacancies`
| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER | Уникальный идентификатор |
| company_id | INTEGER | ID компании (foreign key) |
| name | TEXT | Название вакансии |
| salary | TEXT | Зарплата |
| location | TEXT | Метро/локация |
| link | TEXT | Ссылка на вакансию |
| created_at | TIMESTAMP | Дата добавления |

## Архитектура проекта
Подробно описана в [Архитектура](ARCHITECTURE.md)
