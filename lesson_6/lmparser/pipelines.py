# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy

from pymongo import MongoClient

class LmparserPipeline():
    def __init_(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.materials

    def process_item(self, item, spider):
        result = []
        for i in item['values']:
            result.append(i.strip())
        item['descr'] = dict(zip(item['keys'], result))
        item.pop('keys')
        item.pop('values')

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

class LmPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


