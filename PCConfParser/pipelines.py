# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import gspread
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import csv
import os

#Здесь мы указываем как собираются наши данные

class DataProcessingPipeline:
    def __init__(self):
        self.prices = {}
        self.spiders_count = 0

    def open_spider(self, spider):
        self.spiders_count += 1

        if self.spiders_count == 1:
            # Initialize Google Sheets client only once
            file_name = 'client_key.json'
            client = gspread.service_account(file_name)
            self.sheet = client.open('DemoSheet').worksheet('Лист1')

    def process_item(self, item, spider):
        row_number = item['row_number']
        price = item['price']
        url = item['url']

        if row_number not in self.prices:
            self.prices[row_number] = []

        self.prices[row_number].append(price)

        return item

    def close_spider(self, spider):
        self.spiders_count -= 1

        if self.spiders_count == 0:
            # Update Google Sheet only after all spiders have closed
            for row_number, prices in self.prices.items():
                if prices:
                    lowest_price = min(prices)
                    self.sheet.update_cell(row_number, 11, lowest_price)  # Adjust the column number as needed


#Используя CSVPipeLine -- записываем данные с парсинга в CSV файл
class CsvPipeline(object):
    def open_spider(self, spider):
        # Open file in append mode
        self.file_path = 'output.csv'
        self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)


    def process_item(self, item, spider):
        self.writer.writerow([item['row_number'], item['url'], item['price']])
        return item

    def close_spider(self, spider):
        self.file.close()