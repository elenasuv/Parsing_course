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
    result = vacancies.find({'compensation': {'min': {"$gt": salary}}})
    for vacancy in result:
        pprint(vacancy)

    #pprint(result)
for vacancy in vacancies.find({}):
    pprint(vacancy)


#vacancies_salary()