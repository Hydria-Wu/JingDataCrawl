# -*- coding: utf-8 -*-
# @Time    : 2018/9/22 10:01
# @Author  : hydria
# @Site    :
# @File    : jingData.py
# @Software: PyCharm

import scrapy
import time
import re
import requests
import datetime
import json

from scrapy.http import Request
from selenium import webdriver
from scrapy.selector import Selector
from items import jingDataBaseItem, jingDataItemLoader, jingDataFinanceItem
from selenium.common.exceptions import ElementNotVisibleException
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from DataAnalysis.utils.jingDateUtil import jingdata_cookie, jingdata_id

class JingdataSpider(scrapy.Spider):
    name = 'jingData'
    allowed_domains = ['rong.36kr.com']
    start_urls = ['https://rong.36kr.com/']


    def parse(self, response):
        jingdata = jingdata_id()
        while True:
            # id = '103047'
            id = jingdata.get_id()
            if id is None:
                break
            url = 'https://rong.36kr.com/n/api/company/{}?asEncryptedTs=0.10863102114911757&asTs=1551405890532'
            base_url = url.format(id)
            callback = self.parse_base
            yield Request(base_url, callback, meta={'id': id}, dont_filter=True)

            finance_url = url.format(id + '/finance')
            callback = self.parse_finance
            yield Request(finance_url, callback, meta={'id': id}, dont_filter=True)


    def parse_base(self, response):
        pass
        # 项目id
        # id = response.meta.get('id', '')
        # data = json.loads(response.text)
        # print(data)
        #
        # item_loader = jingDataItemLoader(item=jingDataBaseItem(), response=response)
        # item_loader.add_value('product_id', data['data']['id'])
        # item_loader.add_value('product_name', data['data']['name'])
        # item_loader.add_value('product_brief', data['data']['brief'])
        # item_loader.add_value('start_date_desc', data['data']['startDateDesc'])
        # item_loader.add_value('crawl_time', datetime.datetime.now())
        #
        # article = item_loader.load_item()
        # yield article


    def parse_finance(self, response):
        pass
        # 项目id
        # id = response.meta.get('id', '')
        # data = json.loads(response.text)
        # print(data)
        #
        # item_loader = jingDataItemLoader(item=jingDataFinanceItem(), response=response)
        # item_loader.add_value('product_id', data['data']['id'])
        # item_loader.add_value('crawl_time', datetime.datetime.now())
        #
        # article = item_loader.load_item()
        # yield article



