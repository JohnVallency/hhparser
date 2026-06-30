import sqlite3
import pandas as pd
import re
import os

def extract_number(text):
    """Извлекает число из текста вроде '13 вакансий'"""
    if not text:
        return 0
    match = re.search(r'\d+', text)
    return int(match.group()) if match else 0

def export_top_companies():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hhparser.db')
    
    conn = sqlite3.connect(db_path)

    companies = pd.read_sql_query('''
        SELECT id, name, vacancies_count FROM companies
    ''', conn)
    
    companies['vacancies_num'] = companies['vacancies_count'].apply(extract_number)
    
    top_companies = companies.nlargest(20, 'vacancies_num')
    
    top_companies = top_companies[['name', 'vacancies_count']]
    top_companies.columns = ['Компания', 'Количество вакансий']
    
    company_ids = tuple(companies.nlargest(20, 'vacancies_num')['id'].tolist())
    
    if not company_ids:
        print('❌ В базе нет компаний')
        conn.close()
        return
    
    placeholders = ','.join(['?' for _ in company_ids])
    query = f'''
        SELECT c.name as company_name, c.vacancies_count, 
               v.name as vacancy_name, v.salary, v.location, v.link
        FROM vacancies v
        JOIN companies c ON v.company_id = c.id
        WHERE c.id IN ({placeholders})
        ORDER BY c.name, v.name
    '''
    
    vacancies = pd.read_sql_query(query, conn, params=company_ids)
    conn.close()
    
    vacancies.columns = ['Компания', 'Количество вакансий', 'Вакансия', 'Зарплата', 'Метро', 'Ссылка']
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'top_companies.xlsx')
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        top_companies.to_excel(writer, sheet_name='Топ-20 компаний', index=False)
        vacancies.to_excel(writer, sheet_name='Вакансии топ-20', index=False)
    
    print(f'Excel сохранён: {output_path}')
if __name__ == '__main__':
    export_top_companies()