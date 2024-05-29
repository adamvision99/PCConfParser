import scrapy
from scrapy import Request
import json

class OnlinetradeSpider(scrapy.Spider):
    name = 'onlinetrade'
    allowed_domains = ['onlinetrade.ru']
    start_urls = ['http://onlinetrade.ru/']
    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOADER_MIDDLEWARES": {
            'PCConfParser.middlewares.SeleniumMiddleware': 800
        },
    }

    def __init__(self, urls=None, row_numbers=None):
        self.start_urls = ['https://www.onlinetrade.ru/catalogue/protsessory-c342/intel/protsessor_intel_core_i3_12100f_lga1700_oem_cm8071504651013-2976966.html']
        self.row_numbers = [2]

    def start_requests(self):
        for url, row_number in zip(self.start_urls, self.row_numbers):
          yield Request(url=url, meta={'row_number': row_number})

    def parse(self, response):
        price = response.xpath('//span[@itemprop="price"]/text()').get()
        if price:
            price = price.strip().replace(' ', '')
        else:
            price = 9999999
        yield {
            'site': 'Onlinetrade',
            'url': response.url,
            'price': int(price),
            'row_number': response.meta['row_number']
        }