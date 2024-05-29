import scrapy
from scrapy import Request
import json
class OzonSpider(scrapy.Spider):
    name = 'Ozon'
    allowed_domains = ['ozon.ru']
    start_urls = ['http://ozon.ru/']
    custom_settings = {
        "COOKIES_ENABLED": True,
        'HTTPERROR_ALLOWED_CODES': [500]
    }

    def __init__(self, urls=None, row_numbers=None):
        self.start_urls = urls
        self.row_numbers = row_numbers

    def start_requests(self):
        for url, row_number in zip(self.start_urls, self.row_numbers):
          api_url = "https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=/product/" + url.split('/')[4]
          post_body = {
            "cmd": "request.get",
            "url": api_url,
            "maxTimeout": 60000
          }
          yield Request('http://localhost:8191/v1', method="POST", body=json.dumps(post_body), headers={'Content-Type':'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}, meta={"initial_url": url, "row_number": row_number})

    def parse(self, response):
        data = json.loads(response.body.decode('utf-8'))
        price = data['solution']['response']
        is_price = True
        if price.find('deny_category_prediction') != -1:
          is_price = False
        elif price.find('cardPrice') != -1:
          price = price[price.find('cardPrice'):]
        elif price.rfind('"price\\') != -1:
          price = price[price.rfind('"price\\'):]
        else:
          is_price = False
        if is_price:
          try:
            price = price[:price.find(',')].split(':')[1].split('"')[1].split('₽')[0].replace(u'\u2009', '').replace('\\', '')
          except IndexError:
            price = 99999999
        else:
          price = 1000000000

        yield {
            'site': 'Ozon',
            'url': response.meta['initial_url'],
            'price': int(price),
            'row_number': response.meta['row_number']
        }