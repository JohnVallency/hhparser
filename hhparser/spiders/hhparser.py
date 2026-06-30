import scrapy
from hhparser.hh_db import Database

class HhparserSpider(scrapy.Spider):
    name = 'hhparser'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/employers_list?areaId=1&vacanciesRequired=true']

    def __init__(self):  
        super().__init__()  
        self.db = Database()  
    
    def parse(self, response):
        for company_link in response.css('[data-qa="employer-name"]'):
            company_name = company_link.css('[data-qa="employer-name-text"]::text').get()
            href = company_link.attrib.get('href', '')
            employer_id = href.split('/')[-1]
            vacancies_text = response.css(f'[data-qa="employer-counter-{employer_id}"] ::text').get('')
            search_url = f'https://hh.ru/search/vacancy?employer_id={employer_id}'
            yield scrapy.Request(
            search_url,
            callback=self.parse_employer,
            meta={
                'company_name': company_name,
                'vacancies_count': vacancies_text,
            },
            )
            
        for pages in range(1, 50):
            next_page = f'https://hh.ru/employers_list?query=&areaId=1&vacanciesRequired=true&page={pages}'
            yield response.follow(next_page, callback=self.parse)
    
    def parse_employer(self, response):
        company_name = response.meta['company_name']
        vacancies_count = response.meta['vacancies_count']
        company_id = self.db.save_company(company_name, vacancies_count)
        for card in response.css('[data-qa="vacancy-serp__vacancy"]'):
            salary_parts = card.css('span[class*="magritte-text_typography-label-1-regular"]::text').getall()
            if salary_parts:
                salary = ' '.join(salary_parts).replace('\u202f', '').replace('\xa0', ' ').strip()
            else:
                salary = None
            vacancy_name = card.css('[data-qa="serp-item__title-text"]::text').get() 
            vacancy_location = card.css('[data-qa="address-metro-station-name"]::text').get()  
            vacancy_link = card.css('[data-qa="serp-item__title"]::attr(href)').get()  
            self.db.save_vacancy(company_id, vacancy_name, salary, vacancy_location, vacancy_link)
            yield {
                'company_name': company_name,
                'vacancies_count': vacancies_count,
                'vacancy_name': card.css('[data-qa="serp-item__title-text"]::text').get(),
                'vacancy_salary': salary,
                'vacancy_location': card.css('[data-qa="address-metro-station-name"]::text').get(),
                'vacancy_link': card.css('[data-qa="serp-item__title"]::attr(href)').get(),
            }
    def closed(self, reason):  
        self.db.close()
