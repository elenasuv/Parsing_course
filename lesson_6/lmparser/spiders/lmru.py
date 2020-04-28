# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lmparser.items import LmparserItem


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']
    #start_urls = ['http://leroymerlin.ru/']

    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath(
            "//a[contains(@class,'paginator-button next-paginator-button')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        product_links = response.xpath("//div[@class='product-name']/a/@href").extract()
        for link in product_links:
            yield response.follow(link, callback=self.product_parse)


    def product_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        price = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()").extract_first()
        currency = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='currency']/text()").extract_first()
        unit = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span[@slot='unit']/text()").extract_first()
        photos = response.xpath("//source[@itemprop='image']/@data-origin").extract()
        keys = response.xpath("//dt[@class='def-list__term']/text()").extract()
        values = response.xpath("//div[@class='def-list__group']/dd[@class='def-list__definition']/text()").extract()
        yield LmparserItem(name=name, photos=photos, keys=keys, values=values, price=price, currency=currency, unit=unit)



