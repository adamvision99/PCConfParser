import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings

from spiders import Ozon, DNS, a28bit, onlinetrade
import numpy as np
import multiprocessing
import gspread
import csv


#Сбор данных с гугл таблицы (ссылки на товары и остальное)
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]

file_name = r'C:\Users\Adam\Downloads\Telegram Desktop\PCConfParser\PCConfParser\PCConfParser\client_key.json'
client = gspread.service_account(file_name)

#Fetch the sheet
# sheet = client.open('Конфигуратор ПК').worksheet('Парсинг')
sheet = client.open('DemoSheet').worksheet('Лист1')
sheet_data = sheet.get('G2:J')


#Задаем настройки проекта
settings = get_project_settings()
settings.set('ITEM_PIPELINES', {'PCConfParser.pipelines.CsvPipeline': 1})


#Функция, которая получает ссылки для каждого из сервисов и возвращает в виде списков, где url, номер строки, и название магаза
def get_urls(sheet_data):
    ozon_urls, dns_urls, a28bit_urls, onlinetrade_urls = [], [], [], []
    for row in sheet_data:
        row_number = sheet_data.index(row) + 2
        if len(row) >= 4 and 'ozon' in row[-1]:
            ozon_urls.append({'url': row[-1], 'row_number': row_number, 'spider': 'Ozon'})
        if row and "dns-shop" in row[0]:
            dns_urls.append({'url': row[0], 'row_number': row_number, 'spider': 'DNS'})
        if len(row) >= 3 and '28bit' in row[2]:
            a28bit_urls.append({'url': row[2], 'row_number': row_number, 'spider': '28bit'})
        if len(row) >= 2 and 'onlinetrade' in row[1]:
            onlinetrade_urls.append({'url': row[1], 'row_number': row_number, 'spider': 'onlinetrade'})
    return ozon_urls, dns_urls, a28bit_urls, onlinetrade_urls

#Создаем функцию запуска паресеров как процесс -- метод process.crawl

def run_ozon_spider(ozon_urls):
    process = CrawlerProcess(settings)
    process.crawl(Ozon.OzonSpider, urls=[task['url'] for task in ozon_urls], row_numbers=[task['row_number'] for task in ozon_urls])
    process.start()

def run_a28bit_spider(a28bit_urls):
    process = CrawlerProcess(settings)
    process.crawl(a28bit.A28bitSpider, urls=[task['url'] for task in a28bit_urls], row_numbers=[task['row_number'] for task in a28bit_urls])
    process.start()

def run_dns_spider(dns_urls):
    process = CrawlerProcess(settings)
    process.crawl(DNS.DnsSpider, urls=[task['url'] for task in dns_urls], row_numbers=[task['row_number'] for task in dns_urls])
    process.start()
    
def run_onlinetrade_spider(onlinetrade_urls):
    process = CrawlerProcess(settings)
    process.crawl(onlinetrade.OnlinetradeSpider, urls=[task['url'] for task in onlinetrade_urls], row_numbers=[task['row_number'] for task in onlinetrade_urls])
    process.start()



# Создаем CSV, в которую положим все спарсенные цены


def main():
    file_path = 'output.csv'
    with open(file_path, 'w') as f:
     f.write('Row Number, URL, Price\n')
    ozon_urls, dns_urls, a28bit_urls, onlinetrade_urls = get_urls(sheet_data) #Получаем все наши ссылки (запускаем эту функцию)



# C помощью многопоточности быстро парсишь ОЗОН и 28. Позволяет нам запустить два парсера одновременно и можем контроллировать работу парсеров,
#C помощью multiprocessing

    with multiprocessing.Pool(2) as pool:
        pool.apply_async(run_ozon_spider, [ozon_urls])
        pool.apply_async(run_a28bit_spider, [a28bit_urls])
        pool.close()
        pool.join()


    # with multiprocessing.Pool(2) as pool:
    #     pool.apply_async(run_dns_spider, [dns_urls])
    #     pool.apply_async(run_onlinetrade_spider, [onlinetrade_urls])
    #     pool.close()
    #     pool.join()
    
    dns_process = multiprocessing.Process(target=run_dns_spider, args=(dns_urls,))
    dns_process.start()
    dns_process.join() 

    onlinetrade_process = multiprocessing.Process(target=run_onlinetrade_spider, args=(onlinetrade_urls,))
    onlinetrade_process.start()
    onlinetrade_process.join()

if __name__ == '__main__':
    main()


# Обновляем гугл-таблицу с результатами из парсинга
def update_google_sheet(csv_file):

    # Step 1: Read and Aggregate Prices by Row Number
    prices_by_row = {}
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            row_number = int(row[0])
            url = row[1]
            price = float(row[2])  # Assuming price is in the 3rd column and is a float
            if row_number not in prices_by_row:
                prices_by_row[row_number] = []
            prices_by_row[row_number].append((price, url)) # Записываем переменные

    # Step 2: Find the Lowest Price for Each Row
    lowest_prices = {row: min(prices, key=lambda x: x[0]) for row, prices in prices_by_row.items()}

    # Step 3: Update the Google Sheet with the Lowest Prices
    for row_number, (lowest_price, url) in lowest_prices.items():
        sheet.update_cell(row_number, 11, lowest_price)
        sheet.update_cell(row_number, 12, url)

update_google_sheet('output.csv')