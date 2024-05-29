import scrapy
from scrapy import Request
import time
import json
class DnsSpider(scrapy.Spider):
    name = 'DNS'
    allowed_domains = ['dns-shop.ru']
    start_urls = ['http://dns-shop.ru/']
    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOADER_MIDDLEWARES": {
            'PCConfParser.middlewares.SeleniumMiddleware': 800
        },
    }

    def __init__(self, urls=None, row_numbers=None):
        self.start_urls = urls
        self.row_numbers = row_numbers

    def start_requests(self):
        for url, row_number in zip(self.start_urls, self.row_numbers):
          yield Request(url=url, meta={'row_number': row_number})

    def parse(self, response):
        script_data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        if script_data:
            data = json.loads(script_data)
            price = data['offers']['price']
        else:
            price = 99999999
        yield {
            'site': 'DNS',
            'url': response.url,
            'price': int(price),
            'row_number': response.meta['row_number']
        }