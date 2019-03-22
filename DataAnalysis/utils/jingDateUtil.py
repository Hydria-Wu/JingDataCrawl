#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/22 10:38
# @Author  : hydria
# @Site    : 
# @File    : jingDateUtil.py
# @Software: PyCharm

import datetime
import MySQLdb
import time
import requests
import json
from DataAnalysis.settings import SQL_DATE_FORMAT, SQL_DATETIME_FROMAT
from DataAnalysis.utils.LogUtil import logs
from selenium import webdriver

conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='data_analysis', charset='utf8')
cursor = conn.cursor()

class GetIp(object):
    # 从数据库随机获取IP地址，并对该IP地址进行检验，如果已经失效则删除

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.7 Safari/537.36'}

    def __init__(self):
        self.logging = logs('jingData')

    def delete_ip(self, ip):
        # 删除已经失效的IP地址

        delete_sql = '''
            delete from proxy_ip where ip='{0}'
        '''.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 检验IP地址是否有效

        http_url = 'https://rong.36kr.com/'
        proxy_url = 'http://%s:%s' % (ip, port)
        try:
            proxies = {
                'http': proxy_url,
            }
            response = requests.get(http_url, proxies=proxies, headers=self.headers)
        except Exception as e:
            self.logging.warning('invalid ip and port -- ' + proxy_url)
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code <= 200 and code < 300:
                self.logging.info('effective ip -- ' + proxy_url)
                return True
            else:
                self.logging.warning('invalid ip and port -- ' + proxy_url)
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 随机获取IP地址

        select_sql = 'select ip, port from proxy_ip where proxy_type="HTTP"  order by rand() limit 1'
        result = cursor.execute(select_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return 'http://{0}:{1}'.format(ip, port)
            else:
                return self.get_random_ip()


class jingdata_cookie(object):
    # 轮询法获取cookie，每日自动更新cookie

    lose_list = []
    proxies = {'http': ''}
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.7 Safari/537.36'}

    def __init__(self):
        import random
        self.user = 0
        # self.user = random.randint(1, 210)
        self.logging = logs('jingData')

    def getCookieRandom(self):
        # 轮询法获取cookie

        self.user += 1
        cookie, phone = self.getCookieAndPhone(self.user)
        if cookie == '':
            self.user = 1
            cookie, phone = self.getCookieAndPhone(self.user)
        return cookie, phone

    def getCookie(self):
        # 调用的入口，获取cookie并检验是否有效

        cookie, phone = self.getCookieRandom()
        self.proxies['http'] = self.getProxies()
        if phone in self.lose_list:
            return self.getCookie()

        # 该url需要登陆才能访问成功，用来检测cookie是否有效
        url = 'https://rong.36kr.com/n/api/column/0/company?sortField=HOT_SCORE'
        response = requests.get(url=url, cookies=cookie, headers=self.headers, proxies=self.proxies)
        data = response.json()
        self.sleepRandom()
        if data['code'] == 0:
            return cookie
        else:
            self.lose_list.append(phone)
            self.logging.warning('cookie已失效，phone：' + phone)
            return self.getCookie()

    def getCookieAndPhone(self, id):
        # 从数据库获取cookie和phone

        select_sql = 'select cookie, phone, enter_date from jingdata_account where id={0}'.format(str(id))
        cursor.execute(select_sql)
        obj = cursor.fetchall()
        if obj == ():
            return '', ''
        cookie = obj[0][0]
        phone = obj[0][1]
        enter_date = obj[0][2]

        # 如果cookie不存在或者插入时间不是今天，那么就更新cookie
        if cookie == '' or cookie == None or enter_date < datetime.date.today():
            self.saveOrUpdate(id, phone)
            return self.getCookieAndPhone(id)
        else:
            return json.loads(cookie), phone

    def getProxies(self):
        # 获取代理IP地址

        get_ip = GetIp()
        return get_ip.get_random_ip()

    def sleepRandom(self, num=1):
        # 休眠随机秒数

        import random
        ran = random.randint(0, 2)
        time.sleep(num + ran)

    def saveOrUpdate(self, id, phone):
        # 插入或更新cookie

        cookie = json.dumps(self.getCookieBySelenium(phone))
        cursor.execute(
            """
                insert into jingdata_account(id, cookie, enter_date) VALUES('{0}', '{1}', '{2}')
                ON DUPLICATE KEY UPDATE cookie=VALUES(cookie), enter_date=VALUES(enter_date)
            """.format(
                id, cookie, datetime.date.today().strftime(SQL_DATE_FORMAT)
            )
        )
        conn.commit()

    def getCookieBySelenium(self, phone):
        # selenium模拟登陆，获取已登陆成功的cookie

        option = webdriver.ChromeOptions()
        # 设置参数，不弹出浏览器
        # option.add_argument('--headless')
        # option.add_argument('--disable-gpu')
        browser = webdriver.Chrome(executable_path='C:/Users/hasee/AppData/Local/Google/Chrome/Application/chromedriver.exe',  chrome_options=option)

        browser.get('https://rong.36kr.com/')

        # 在首页点击登录按钮，进入登录界面
        browser.find_element_by_css_selector('span.icon-login').click()

        time.sleep(5)

        # 输入用户名和密码，并点击登录
        browser.find_element_by_css_selector('input[name=username]').send_keys(phone)
        browser.find_element_by_css_selector('input[name=password]').send_keys('')
        browser.find_element_by_css_selector('button[type=submit]').click()

        cookie = {}

        # 等待10秒钟
        time.sleep(10)

        # 获取cookie
        cookies = browser.get_cookies()
        for cki in cookies:
            cookie[cki['name']] = cki['value']

        # 关闭浏览器
        browser.quit()

        return cookie


class jingdata_id(object):
    # 从数据库获取项目id

    def get_id(self):
        # 随机获取未爬取过的项目id

        select_sql = 'select product_id from jingdata_spider where product_brief!=0 order by rand() limit 1'
        result = cursor.execute(select_sql)
        if result == 1:
            id = cursor.fetchall()[0][0]
            update_sql = 'UPDATE jingdata_spider SET product_brief=0 where product_id={0}'.format(id)
            cursor.execute(update_sql, ())
            conn.commit()

            cursor.execute(
                """
                    insert into project(project_id, project_name, project_des, industry, city, year, crawl_time)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')
                """.format(
                    id, 'a', 'a', 'a', 'a', 'a', datetime.datetime.now().strftime(SQL_DATETIME_FROMAT)
                )
            )
            conn.commit()
            return id

    def delete_id(self, id):
        # 删除已经失效的ID

        delete_sql = '''
            delete from jingdata_spider where product_id='{0}'
        '''.format(id)
        cursor.execute(delete_sql)
        conn.commit()

        delete_sql = '''
            delete from project where project_id='{0}'
        '''.format(id)
        cursor.execute(delete_sql)
        conn.commit()


if __name__ == '__main__':
    jingdata = jingdata_cookie()
    for i in range(1, 212):
        print(i)
        jingdata.getCookieRandom()
