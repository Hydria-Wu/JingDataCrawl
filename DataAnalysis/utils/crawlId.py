#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/23 16:51
# @Author  : hydria
# @Site    : 
# @File    : crawlId.py
# @Software: PyCharm

import datetime
import MySQLdb
import time
import requests

from settings import SQL_DATETIME_FROMAT
from fake_useragent import UserAgent
from DataAnalysis.utils.jingDateUtil import GetIp, jingdata_cookie
from DataAnalysis.utils.LogUtil import logs

conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='data_analysis', charset='utf8')
cursor = conn.cursor()


class jingdata_id(object):
    # 获取所有项目的id

    # 行业
    industry_list = ['industry.E_COMMERCE', 'industry.SOCIAL_NETWORK', 'industry.INTELLIGENT_HARDWARE', 'industry.MEDIA', 'industry.SOFTWARE', 'industry.CONSUMER_LIFESTYLE', 'industry.FINANCE', 'industry.MEDICAL_HEALTH', 'industry.SERVICE_INDUSTRIES', 'industry.TRAVEL_OUTDOORS', 'industry.PROPERTY_AND_HOME_FURNISHINGS', 'industry.EDUCATION_TRAINING', 'industry.AUTO', 'industry.LOGISTICS', 'industry.AI', 'industry.UAV', 'industry.ROBOT', 'industry.VR_AR', 'industry.SPORTS', 'industry.FARMING', 'industry.SHARE_BUSINESS', 'industry.CHU_HAI', 'industry.CONSUME']
    # 城市
    city_list = ['city.101', 'city.109', 'city.21903', 'city.21901', 'city.21101', 'city.22301', 'city.102', 'city.90000', 'city.122', 'city.112', 'city.113', 'city.128', 'city.119', 'city.120', 'city.124', 'city.121', 'city.103', 'city.116', 'city.108', 'city.117', 'city.118', 'city.107', 'city.110', 'city.114', 'city.106', 'city.130', 'city.129', 'city.115', 'city.104', 'city.127', 'city.123', 'city.125', 'city.111', 'city.105', 'city.131', 'city.126', 'city.133', 'city.134', 'city.132']
    # 融资轮次
    phase_list = ['phase.SEED', 'phase.ANGEL', 'phase.PRE_A', 'phase.A', 'phase.A_PLUS', 'phase.PRE_B', 'phase.B', 'phase.B_PLUS', 'phase.C', 'phase.C_PLUS', 'phase.D', 'phase.E', 'phase.INFORMAL', 'phase.PRIVATE_REPLACEMENT', 'phase.AFTER_IPO', 'phase.PRE_IPO', 'phase.ACQUIRED']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.7 Safari/537.36'}

    proxies = {'http': ''}

    lose_list = []

    count = 0

    def __init__(self):
        self.account = jingdata_cookie()
        self.get_ip = GetIp()
        self.logging = logs('jingData')

    def getCookie(self):
        return self.account.getCookie()

    def setHeaders(self):
        self.headers['User-Agent'] = getattr(UserAgent(), 'random')

    def setProxies(self):
        self.proxies['http'] = self.get_ip.get_random_ip()

    def setSettings(self):
        self.setProxies()
        self.setHeaders()

    def sleepForMinute(self, num=10):
        for i in range(num):
            time.sleep(60)
            self.logging.info('睡眠' + str(i + 1) + '分钟')

    def sleepRandom(self, num=5):
        import random
        ran = random.randint(1, 5)
        time.sleep(num + ran)

    def jingdata_id(self):
        # 获取id，根据行业、城市、融资轮次三个选项进行细分
        # 根据这种请求方式获取的项目，鲸准不提供超过1000个项目，所以需要细分
        # 融资轮次中没有‘未融资’选项，所以会有大量未融资的项目不会爬取
        # 请注意，这种方式爬取不到所有的项目，但大部分项目都可以爬取

        url = 'https://rong.36kr.com/n/api/column/0/company?sortField=HOT_SCORE'
        for i in range(len(self.industry_list)):
            cookie, phone = self.getCookie()
            industry = self.industry_list[i]
            post_url_industry = url + '&' + industry.replace('.', '=')
            self.setSettings()
            response = requests.get(url=post_url_industry, cookies=cookie, headers=self.headers, proxies=self.proxies)
            data = response.json()
            totalCount = data['data']['pageData']['totalCount']
            self.sleepRandom(5)

            # 如果该行业下的项目超过了1000个，则加入城市
            if totalCount > 1000:
                for c in range(len(self.city_list)):
                    cookie, phone = self.getCookie()
                    city = self.city_list[c]
                    post_url_city = post_url_industry + '&' + city.replace('.', '=')
                    self.setSettings()
                    response = requests.get(url=post_url_city, cookies=cookie, headers=self.headers, proxies=self.proxies)
                    data = response.json()
                    totalCount = data['data']['pageData']['totalCount']
                    self.sleepRandom(5)

                    # 如果该行业、城市下的项目超过了1000个，则加入融资轮次
                    if totalCount > 1000:
                        for p in range(len(self.phase_list)):
                            cookie, phone = self.getCookie()
                            phase = self.phase_list[p]
                            post_url_phase = post_url_city + '&' + phase.replace('.', '=')
                            self.setSettings()
                            response = requests.get(url=post_url_phase, cookies=cookie, headers=self.headers, proxies=self.proxies)
                            data = response.json()
                            totalCount = data['data']['pageData']['totalCount']
                            self.sleepRandom(5)

                            # 如果该行业、城市、融资轮次下的项目超过了1000个，则打印warning级别的日志输出
                            if totalCount > 1000:
                                self.logging.warning('------' + str(industry) + ', ' + str(city) + ', ' + str(phase) + ', ' + str(totalCount))
                            self.saveAll(post_url_phase)
                    else:
                        self.saveAll(post_url_city)
            else:
                self.saveAll(post_url_industry)

    def saveAll(self, url):
        # 进入该方法的url不会超过1000个项目，五十次请求将所有项目爬取

        cookie, phone = self.getCookie()
        for i in range(1, 51):
            post_url = url + '&p=' + str(i)
            self.setSettings()
            response = requests.get(url=post_url, cookies=cookie, headers=self.headers, proxies=self.proxies)
            data = response.json()
            try:
                dataJson = data['data']['pageData']['data']
            except KeyError:
                self.logging.error('cookie已失效，phone：' + phone)
                dataJson = data['data']['pageData']['data']
            if dataJson == []:
                break
            self.save(dataJson)
            self.count += len(dataJson)
            self.sleepRandom(5)
        self.logging.info('保存成功, url: ' + url + ', 第' + str(self.count) + '个项目')


    def save(self, data):
        # 保存到数据库

        list = []

        for i in range(len(data)):
            product_id = data[i]['id']
            crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FROMAT)

            list.append((product_id, crawl_time))

        # 批量插入
        params = tuple(list)
        sql = """
                INSERT INTO jingdata_spider(product_id, crawl_time) VALUES(%s, %s)
                ON DUPLICATE KEY UPDATE crawl_update_time=VALUES(crawl_time)
              """
        cursor.executemany(sql, params)
        conn.commit()

if __name__ == '__main__':
    jingdata = jingdata_id()
    jingdata.jingdata_id()












