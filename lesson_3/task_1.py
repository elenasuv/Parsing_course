from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re


vacancy = 'python'

#главные страницы сайтов
main_link_1 = 'https://hh.ru'
main_link_2 = 'https://russia.superjob.ru'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}



# функция для парсинга вакансий с одной страницы hh.ru
def vacancies_hh(hh_list):
    vacancies_hh = []
    for vacancy_hh in hh_list:
        vacancy_hh_data = {}
        vacancy_hh_compensation={}
        vacancy_hh_link = vacancy_hh.find('a')['href']
        vacancy_hh_name = vacancy_hh.find('a').getText()
        vacancy_hh_data['link'] = vacancy_hh_link
        vacancy_hh_data['name'] = vacancy_hh_name
        vacancy_hh_data['source'] = 'hh.ru'
        compensation = vacancy_hh.find('span',{'data-qa': 'vacancy-serp__vacancy-compensation'})
        if compensation:
            vacancy_hh_price = compensation.getText()
            if '-' in vacancy_hh_price:
                vacancy_hh_min_price_text, vacancy_hh_max_price_text = vacancy_hh_price.split('-')
                vacancy_hh_min_price = int(''.join(re.findall('\d+', vacancy_hh_min_price_text)))
                vacancy_hh_max_price = int(''.join(re.findall('\d+', vacancy_hh_max_price_text)))
                vacancy_hh_compensation['min'] = vacancy_hh_min_price
                vacancy_hh_compensation['max'] = vacancy_hh_max_price
            elif 'от' in vacancy_hh_price:
                vacancy_hh_min_price = int(''.join(re.findall('\d+', vacancy_hh_price)))
                vacancy_hh_compensation['min'] = vacancy_hh_min_price
                vacancy_hh_compensation['max'] = 'NaN'
                vacancy_hh_price = vacancy_hh_price.replace('от', '')
            elif 'до' in vacancy_hh_price:
                vacancy_hh_max_price = int(''.join(re.findall('\d+', vacancy_hh_price)))
                vacancy_hh_compensation['min'] = 'NaN'
                vacancy_hh_compensation['max'] = vacancy_hh_max_price
                vacancy_hh_price = vacancy_hh_price.replace('до', '')
            vacancy_hh_currency = re.findall('[А-Я,а-я,A-Z,a-z]+\.?', vacancy_hh_price)[0]
            vacancy_hh_compensation['currency'] = vacancy_hh_currency
            vacancy_hh_data['compensation'] = vacancy_hh_compensation
        else:
            vacancy_hh_data['compensation'] = 'NaN'

        vacancies_hh.append(vacancy_hh_data)
    return(vacancies_hh)



# функция для парсинга вакансий со всех страниц hh.ru
def all_hh_links():
    html_hh = requests.get(main_link_1 + '/search/vacancy?area=&st=searchVacancy&text=' + vacancy, headers=header, verify=False).text
    soup_hh = bs(html_hh, 'html.parser')
    max_button = int(soup_hh.find_all('a', {'class':'bloko-button HH-Pager-Control'})[-1].getText())
    vacancies_hh_links = [main_link_1 + '/search/vacancy?area=&st=searchVacancy&text=' + vacancy + '&page='+ str(i) for i in range(0,max_button)]
    for link in vacancies_hh_links:
        html = requests.get(link, headers=header,
                        verify=False).text
        soup = bs(html, 'html.parser')
        vacancies_hh_block = soup.find_all('div', {
            'class': 'bloko-column bloko-column_l-13 bloko-column_m-9 bloko-column_s-8 bloko-column_xs-4'})[0]
        vacancies_hh_list = soup.find_all('div', {'class': 'vacancy-serp-item'})
        return (vacancies_hh(vacancies_hh_list))

# функция для парсинга вакансий с одной страницы superjob.ru
def vacancies_sj(superjob_list):
    vacancies_sj = []
    for vacancy_sj in superjob_list:
        vacancy_sj_data = {}
        vacancy_sj_compensation = {}
        vacancy_sj_link = main_link_2 + vacancy_sj.find('a')['href']
        vacancy_sj_name = vacancy_sj.find('a').getText()
        vacancy_sj_data['link'] = vacancy_sj_link
        vacancy_sj_data['name'] = vacancy_sj_name
        vacancy_sj_data['source'] = 'superjob.ru'
        vacancy_sj_price = vacancy_sj.find('span', {'class': '_3mfro _2Wp8I _31tpt f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).getText()
        vacancy_sj_data['compensation'] = vacancy_sj_compensation
        if '-' in vacancy_sj_price:
            vacancy_sj_min_price_text, vacancy_sj_max_price_text = vacancy_sj_price.split('-')
            vacancy_sj_min_price = int(''.join(re.findall('\d+', vacancy_sj_min_price_text)))
            vacancy_sj_max_price = int(''.join(re.findall('\d+', vacancy_sj_max_price_text)))
            vacancy_sj_compensation['min'] = vacancy_sj_min_price
            vacancy_sj_compensation['max'] = vacancy_sj_max_price
        elif 'от' in vacancy_sj_price:
            vacancy_sj_min_price = int(''.join(re.findall('\d+', vacancy_sj_price)))
            vacancy_sj_compensation['min'] = vacancy_sj_min_price
            vacancy_sj_compensation['max'] = 'NaN'
            vacancy_sj_price = vacancy_sj_price.replace('от', '')
            vacancy_sj_currency = re.findall('[А-Я,а-я,A-Z,a-z]+\.?', vacancy_sj_price)[0]
            vacancy_sj_compensation['currency'] = vacancy_sj_currency
        elif re.findall('до\s', vacancy_sj_price):
            vacancy_sj_max_price = int(''.join(re.findall('\d+', vacancy_sj_price)))
            vacancy_sj_compensation['min'] = 'NaN'
            vacancy_sj_compensation['max'] = vacancy_sj_max_price
            vacancy_sj_price = vacancy_sj_price.replace('до', '')
            vacancy_sj_currency = re.findall('[А-Я,а-я,A-Z,a-z]+\.?', vacancy_sj_price)[0]
            vacancy_sj_compensation['currency'] = vacancy_sj_currency
        else:
            vacancy_sj_data['compensation'] = 'По договоренности'

        vacancies_sj.append(vacancy_sj_data)
    return(vacancies_sj)

# функция для парсинга вакансий со всех страниц superjob.ru
def all_sj_links():
    html_sj = requests.get(main_link_2 + '/vacancy/search/?keywords='+vacancy, headers=header,
                           verify=False).text
    soup_sj = bs(html_sj, 'html.parser')
    max_button = int(soup_sj.find_all('span', {'class': '_3IDf-'})[-3].getText())
    vacancies_sj_links = [main_link_2 + '/vacancy/search/?keywords='+vacancy + '&page='+ str(i) for i in range(1,max_button)]
    for link in vacancies_sj_links:
        html = requests.get(link, headers=header,
                            verify=False).text
        soup_1 = bs(html, 'html.parser')
        vacancies_sj_block = soup_1.find_all('div', {'class': '_1ID8B'})[0]
        vacancies_sj_list = vacancies_sj_block.find_all('div', {'class': '_3zucV f-test-vacancy-item _3j3cA RwN9e _3tNK- _1NStQ _1I1pc'})
        return(vacancies_sj(vacancies_sj_list))



a = all_hh_links()
b = all_sj_links()





