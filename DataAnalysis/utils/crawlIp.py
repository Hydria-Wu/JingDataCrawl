#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/22 16:51
# @Author  : hydria
# @Site    : 
# @File    : crawlIp.py
# @Software: PyCharm

import requests
import MySQLdb

conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='article_spider', charset='utf8')
cursor = conn.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
}

def crawl_pro_ips():
    # 爬取西瓜代理的付费ip（吐槽一句，不是很稳定，建议用其他的代理 =，=）

    # tid是付费获取的
    tid = '556611573747003'
    url = 'http://api3.xiguadaili.com/ip/?tid={}&num=1000&category=2&delay=1&protocol=http'.format(tid)
    response = requests.get(url=url, headers=headers)

    ip_list = response.text.split('\r\n')

    for ip in ip_list:
        ip_info = ip.split(':')
        cursor.execute(
            """
                insert proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', '1', 'HTTP')
                ON DUPLICATE KEY UPDATE speed=VALUES(speed), proxy_type=VALUES(proxy_type)
            """.format(
                ip_info[0], ip_info[1]
            )
        )
        conn.commit()


if __name__ == '__main__':
    crawl_pro_ips()













