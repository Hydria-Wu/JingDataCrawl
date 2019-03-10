# -*- coding: utf-8 -*-
# @Time    : 2018/9/22 09:01
# @Author  : hydria
# @Site    :
# @File    : jingData.py
# @Software: PyCharm

import time
import scrapy
import datetime
import json

from scrapy.http import Request
from DataAnalysis.items import ProjectItem, jingDataItemLoader, FinanceRoundItem, ProjectLabelItem
from DataAnalysis.utils.DateUtil import timestamp_to_format
from DataAnalysis.utils.jingDateUtil import jingdata_id
from DataAnalysis.utils.LogUtil import logs
from DataAnalysis.enum.industryEnum import industry
from DataAnalysis.enum.phaseEnum import phase

class JingdataSpider(scrapy.Spider):
    name = 'jingData'
    allowed_domains = ['rong.36kr.com']
    start_urls = ['https://rong.36kr.com/']


    def __init__(self):
        self.logging = logs('jingData')
        self.jingdata = jingdata_id()


    def parse(self, response):
        # 页面由纯js加载，所以只能模拟ajax请求
        # 经过分析，爬取分为两步，先爬取所有项目的id，再根据id获取需要的信息

        while True:
            # 从数据库获取项目
            id = self.jingdata.get_id()
            if id is None:
                break

            url = 'https://rong.36kr.com/n/api/company/{}?asEncryptedTs=0.10863102114911757&asTs=1551405890532'

            # 获取项目的信息
            project_url = url.format(id)
            yield Request(project_url, callback=self.parse_project, meta={'id': id}, dont_filter=True)

            # 获取融资轮次的信息
            finance_url = url.format(id + '/finance')
            yield Request(finance_url, callback=self.parse_finance, meta={'id': id}, dont_filter=True)


    def parse_project(self, response):
        # 项目id
        id = response.meta.get('id', '')
        data = json.loads(response.text)
        if data['code'] == 404:
            self.jingdata.delete_id(id)
            self.logging.warning('公司不存在。id: ' + id)
            return

        self.logging.info('project_url: ' + response.url)
        self.logging.info('project_data: ' + str(data))

        # 项目信息
        item_loader = jingDataItemLoader(item=ProjectItem(), response=response)
        item_loader.add_value('project_id', data['data']['id'])
        item_loader.add_value('project_name', data['data']['name'])
        item_loader.add_value('project_des', data['data']['brief'])
        item_loader.add_value('industry', industry[data['data']['industryEnum']].value)
        item_loader.add_value('city', data['data']['address1Desc'])

        try:
            item_loader.add_value('year', data['data']['startDateDesc'])
        except:
            self.logging.warning('该项目没有日期，id: ' + id)
            item_loader.add_value('year', '1970')
        item_loader.add_value('crawl_time', datetime.datetime.now())

        article = item_loader.load_item()
        yield article

        operationTag = data['data']['operationTag']
        industryTag = data['data']['industryTag']
        operationTag.extend(industryTag)
        for i in range(len(operationTag)):

            # 项目标签
            item_loader = jingDataItemLoader(item=ProjectLabelItem(), response=response)
            item_loader.add_value('project_id', data['data']['id'])
            item_loader.add_value('label_num', str(data['data']['id']) + self.setStr(i + 1))
            item_loader.add_value('label', operationTag[i]['name'])
            item_loader.add_value('crawl_time', datetime.datetime.now())

            article = item_loader.load_item()
            yield article


    def parse_finance(self, response):
        # 项目id
        id = response.meta.get('id', '')
        data = json.loads(response.text)
        if data['data'] == []:
            return
        self.logging.info('finance_url: ' + response.url)
        self.logging.info('finance_data: ' + str(data))

        finance_list = data['data'][::-1]

        for i in range(len(finance_list)):

            # 项目融资轮次
            item_loader = jingDataItemLoader(item=FinanceRoundItem(), response=response)
            item_loader.add_value('project_id', int(id))
            item_loader.add_value('round_num',  id + self.setStr(i + 1))
            item_loader.add_value('round_year', timestamp_to_format(finance_list[i]['financeDate'] / 1000))
            item_loader.add_value('financing_round', phase[finance_list[i]['phase']].value)
            item_loader.add_value('crawl_time', datetime.datetime.now())

            article = item_loader.load_item()
            yield article


    def sleepRandom(self, num=1):
        import random
        ran = random.randint(0, 1)
        time.sleep(num + ran)


    def setStr(self, num):
        if num < 10:
            return '0' + str(num)
        else:
            return str(num)


