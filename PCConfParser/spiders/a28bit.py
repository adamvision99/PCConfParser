import scrapy
from scrapy import Request

class A28bitSpider(scrapy.Spider):
    name = '28bit'
    allowed_domains = ['28bit.ru']

    def __init__(self, urls=None, row_numbers=None):
        self.start_urls = urls
        self.row_numbers = row_numbers

    def start_requests(self):
        for url, row_number in zip(self.start_urls, self.row_numbers):
          yield Request(url=url, meta={'row_number': row_number})

    def parse(self, response):
        price = response.xpath('//div[@class="price product__price"]/text()').get().strip().replace(' ', '')
        yield {
            'site': '28bit',
            'url': response.url,
            'price': int(price),
            'row_number': response.meta['row_number']
        }