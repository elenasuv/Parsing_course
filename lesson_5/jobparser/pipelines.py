# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies_1

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            self.salary_hh(item)
        else:
            self.salary_sj(item)
        item.pop('salary')
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item



    def salary_hh(self, item):
        item['site'] = 'hh.ru'
        if len(item['salary']) >= 6:
            item['salary_min'] = int(item['salary'][1].replace('\xa0', ''))
            item['salary_max'] = int(item['salary'][3].replace('\xa0', ''))
            item['currency'] = item['salary'][5]
        elif len(item['salary']) < 6:
            if item['salary'][0] == 'от ':
                item['salary_min'] = int(item['salary'][1].replace('\xa0', ''))
                item['salary_max'] = 'NaN'
                item['currency'] = item['salary'][3]
            elif item['salary'][0] == 'до ':
                item['salary_min'] = 'NaN'
                item['salary_max'] = int(item['salary'][1].replace('\xa0', ''))
                item['currency'] = item['salary'][3]
            else:
                item['salary_min'] = 'NaN'
                item['salary_max'] = 'NaN'
                item['currency'] = 'NaN'



    def salary_sj(self, item):
        item['site'] = 'superjob.ru'
        if len(item['salary']) >= 6:
            item['salary_min'] = int(item['salary'][0].replace('\xa0', ''))
            item['salary_max'] = int(item['salary'][4].replace('\xa0', ''))
            item['currency'] = item['salary'][6]
        elif len(item['salary']) < 6:
            if item['salary'][0] == 'от':
                sj_salary_split = item['salary'][2].split('\xa0')
                item['salary_min'] = int(''.join(sj_salary_split[:-1]))
                item['salary_max'] = 'NaN'
                item['currency'] = sj_salary_split[-1]
            elif item['salary'][0] == 'до':
                sj_salary_split = item['salary'][2].split('\xa0')
                item['salary_min'] = 'NaN'
                item['salary_max'] = int(''.join(sj_salary_split[:-1]))
                item['currency'] = sj_salary_split[-1]
            else:
                item['salary_min'] = 'NaN'
                item['salary_max'] = 'NaN'
                item['currency'] = 'NaN'














