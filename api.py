from fastapi import FastAPI, HTTPException
from hhparser.hh_db import Database

app = FastAPI(title="HH Parser API", description="API для получения данных о вакансиях и компаниях")
db = Database()

@app.get("/")
def root():
    return {"message": "HH Parser API", "docs": "/docs", "companies" : "/companies", "vacancies" : "/vacancies"}

@app.get("/companies")
def get_companies():
    companies = db.get_all_companies()
    return {"count": len(companies), "companies": companies}

@app.get("/companies/{company_id}")
def get_company(company_id: int):
    company = db.get_company_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.get("/vacancies")
def get_vacancies():
    vacancies = db.get_all_vacancies()
    return {"count": len(vacancies), "vacancies": vacancies}

@app.get("/vacancies/{vacancy_id}")
def get_vacancy(vacancy_id: int):
    vacancy = db.get_vacancy_by_id(vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return vacancy

@app.get("/vacancies/by-company/{company_id}")
def get_vacancies_by_company(company_id: int):
    company = db.get_company_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    vacancies = db.get_vacancies_by_company(company_id)
    return {
        "company": company,
        "count": len(vacancies),
        "vacancies": vacancies
    }

@app.on_event("shutdown")
def shutdown_event():
    db.close()