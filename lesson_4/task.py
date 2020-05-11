from lxml import html
from requests import get
from pprint import pprint
import re
from pymongo import MongoClient
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

#функция для парсинга yandex news
def request_to_yandex_news():
    main_link = 'https://yandex.ru'
    response = get('https://yandex.ru/news/',
                   headers = header, verify = False
                   )

    root = html.fromstring(response.text)
    result = []
    items = root.xpath("//td[@class='stories-set__item'] | //div[@class='stories-set__main-item']")
    for item in items:
        info = {}
        link = main_link + item.xpath(".//div[contains(@class, 'story__topic')]//h2/a/@href")[0]
        name = item.xpath(".//div[contains(@class, 'story__topic')]//h2/a//text()")[0]
        source_time = item.xpath(".//div[contains(@class, 'story__date')]//text()")[0].replace('\xa0', ' ').split()
        source = ''.join(source_time[:-1])
        time = ''.join(source_time[-1])
        info['link'] = link
        info['name'] = name
        info['source'] = source
        info['time'] = time
        result.append(info)
    return result



#функция для парсинга mail news
def request_to_mail_news():
    main_link = 'https://news.mail.ru'
    response = get('https://news.mail.ru/',
                headers = header, verify = False
                )

    root = html.fromstring(response.text)
    full_links_list = []
    links = root.xpath("//div[@class='daynews__item']//a/@href | "
                   "//div[@class='daynews__item daynews__item_big']//a/@href  |"
                   " //ul[@class='list list_type_square list_half js-module']/li[contains(@class,'list__item')]/a/@href")
    for link in links:
        full_link = main_link + link
        full_links_list.append(full_link)

    result = []
    for link in full_links_list:
        info = {}
        response = get(link,
                   headers=header, verify=False
                   )
        root = html.fromstring(response.text)
        link = response.url
        name = root.xpath("//h1[@class='hdr__inner']//text()")[0]
        source = root.xpath("//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']//text()")[0]
        time = root.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]
        info['link'] = link
        info['name'] = name
        info['source'] = source
        info['time'] = time
        result.append(info)
    return(result)


#функция для парсинга lenta.ru
def request_to_lenta_ru():
    main_link = 'https://lenta.ru'
    response = get('https://lenta.ru/',
                headers=header, verify=False
                 )
    root = html.fromstring(response.text)
    result = []
    items = root.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[contains(@class,'item')]")
    for item in items:
        info = {}
        link = main_link + item.xpath(".//a/@href")[0]
        name = item.xpath(".//a//text()")[1].replace('\xa0', ' ')
        time = item.xpath(".//time/@datetime")[0]
        info['link'] = link
        info['name'] = name
        info['source'] = 'lenta.ru'
        info['time'] = time
        result.append(info)
    return(result)



result_1 = request_to_yandex_news()
#pprint(result_1)
result_2 = request_to_mail_news()
#pprint(result_2)
result_3 = request_to_lenta_ru()
#pprint(result_3)

#Сохранение результатов в базе данных
client = MongoClient('localhost', 27017)
db = client['database']
news = db.news

def get_news():
    news.insert_many(request_to_yandex_news())
    news.insert_many(request_to_mail_news())
    news.insert_many(request_to_lenta_ru())

#get_news()

for i in news.find({}):
    pprint(i)
