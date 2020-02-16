# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os

class WbtcPipeline(object):
    def __init__(self):
        # csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/spiders/wbtc.csv'
        print("***************************************************************")
        # 打开(创建)文件

        self.file = open(store_file, mode='a+', encoding="utf-8-sig",newline='')
        # csv写法
        self.writer = csv.writer(self.file, dialect="excel")

    def process_item(self, item, spider):
        print("正在写入......")
        self.writer.writerow([item['describe'],item['city'],item['area'],item['rent']])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()

class WbtcPipeline_zf(object):
    def __init__(self):
        # csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/spiders/wbtc_zf.csv'
        print("***************************************************************")
        # 打开(创建)文件

        self.file = open(store_file, mode='a+', encoding="utf-8-sig",newline='')
        # csv写法
        self.writer = csv.writer(self.file, dialect="excel")

    def process_item(self, item, spider):
        print("正在写入......")
        self.writer.writerow([item['describe'],item['city'],item['area'],item['rent']])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()
