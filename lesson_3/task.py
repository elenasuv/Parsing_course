from pymongo import MongoClient
from pprint import pprint
import task_1
#Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД


client = MongoClient('localhost', 27017)
db = client['database']
vacancies = db.vacancies

def get_vacancies():
    vacancies.insert_many(task_1.all_hh_links())
    vacancies.insert_many(task_1.all_sj_links())

    for vacancy in vacancies.find({}):
        pprint(vacancy)
#get_vacancies()


#Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы
def vacancies_salary():
    salary = input('Введите минимальный порог заработной платы для Вас: ')
    result = vacancies.find({'$or':[{'compensation.min': {"$gt": int(salary)}},
                                    {'compensation.max': {"$gt": int(salary)}}
                                    ]})
    for vacancy in result:
        pprint(vacancy)

#vacancies_salary()

#Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта
def vacancies_update():
    for i in task_1.all_hh_links():
        vacancies.update_one({'link': i['link']}, {'$set': i}, upsert = True)
    for i in task_1.all_sj_links():
        vacancies.update_one({'link': i['link']}, {'$set': i}, upsert = True)
    for vacancy in vacancies.find({}):
        pprint(vacancy)

vacancies_update()


