import sqlite3

class Database:
    def __init__(self, db_name='hhparser.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                vacancies_count TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                name TEXT NOT NULL,
                salary TEXT,
                location TEXT,
                link TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id)
            )
        ''')
        
        self.conn.commit()
    
    def save_company(self, name, vacancies_count):
        self.cursor.execute('''
            INSERT INTO companies (name, vacancies_count)
            VALUES (?, ?)
        ''', (name, vacancies_count))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def save_vacancy(self, company_id, name, salary, location, link):
        self.cursor.execute('''
            INSERT INTO vacancies (company_id, name, salary, location, link)
            VALUES (?, ?, ?, ?, ?)
        ''', (company_id, name, salary, location, link))
        self.conn.commit()
    
    def get_all_companies(self):
        self.cursor.execute('SELECT id, name, vacancies_count, created_at FROM companies ORDER BY id')
        return [dict(zip(['id', 'name', 'vacancies_count', 'created_at'], row)) 
                for row in self.cursor.fetchall()]
    
    def get_company_by_id(self, company_id):
        self.cursor.execute('SELECT id, name, vacancies_count, created_at FROM companies WHERE id = ?', (company_id,))
        row = self.cursor.fetchone()
        return dict(zip(['id', 'name', 'vacancies_count', 'created_at'], row)) if row else None
    
    def get_all_vacancies(self):
        self.cursor.execute('''
            SELECT v.id, c.name as company_name, v.name, v.salary, v.location, v.link, v.created_at
            FROM vacancies v JOIN companies c ON v.company_id = c.id ORDER BY v.id
        ''')
        return [dict(zip(['id', 'company_name', 'name', 'salary', 'location', 'link', 'created_at'], row)) 
                for row in self.cursor.fetchall()]
    
    def get_vacancy_by_id(self, vacancy_id):
        self.cursor.execute('''
            SELECT v.id, c.name as company_name, v.name, v.salary, v.location, v.link, v.created_at
            FROM vacancies v JOIN companies c ON v.company_id = c.id WHERE v.id = ?
        ''', (vacancy_id,))
        row = self.cursor.fetchone()
        return dict(zip(['id', 'company_name', 'name', 'salary', 'location', 'link', 'created_at'], row)) if row else None
    
    def get_vacancies_by_company(self, company_id):
        self.cursor.execute('''
            SELECT v.id, c.name as company_name, v.name, v.salary, v.location, v.link, v.created_at
            FROM vacancies v JOIN companies c ON v.company_id = c.id WHERE v.company_id = ?
        ''', (company_id,))
        return [dict(zip(['id', 'company_name', 'name', 'salary', 'location', 'link', 'created_at'], row)) 
                for row in self.cursor.fetchall()]
    
    def close(self):
        self.conn.close()