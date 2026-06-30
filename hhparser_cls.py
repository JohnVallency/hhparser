import subprocess
import sys
import os

def get_project_dir():
    return os.path.dirname(os.path.abspath(__file__))

def install_dependencies():
    print("=" * 60)
    print("Шаг 1/3: Установка зависимостей...")
    print("=" * 60)
    
    project_dir = get_project_dir()
    requirements_path = os.path.join(project_dir, 'requirements.txt')
    
    if not os.path.exists(requirements_path):
        print(f"Файл requirements.txt не найден: {requirements_path}")
        return False
    
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", requirements_path],
        cwd=project_dir
    )
    
    if result.returncode != 0:
        print("Ошибка при установке зависимостей")
        return False
    
    print(" Зависимости установлены\n")
    return True

def run_parser():
    print("=" * 60)
    print("Шаг 2/3: Запуск парсера...")
    print("=" * 60)
    
    project_dir = get_project_dir()
    
    result = subprocess.run(
        [sys.executable, "-m", "scrapy", "crawl", "hhparser"],
        cwd=project_dir
    )
    
    if result.returncode != 0:
        print("Парсинг завершился с ошибкой")
        return False
    
    print("Парсинг завершён успешно\n")
    return True

def run_api():
    print("=" * 60)
    print("Шаг 3/3: Запуск API...")
    print("Документация: http://127.0.0.1:8000/docs")
    print("Компании:    http://127.0.0.1:8000/companies")
    print("Вакансии:    http://127.0.0.1:8000/vacancies")
    print("=" * 60)
    print("Для остановки нажмите Ctrl+C\n")
    
    project_dir = get_project_dir()
    
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=project_dir
    )

def main():
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║       HH Parser — Парсинг с hh.ru                    ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    
    
    if not install_dependencies():
        sys.exit(1)
    
    
    if not run_parser():
        sys.exit(1)
    
    
    run_api()

if __name__ == "__main__":
    main()