#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/13 16:33
# @Author  : hydria
# @Site    : 
# @File    : LogUtil.py
# @Software: PyCharm

import datetime, os, logging
from DataAnalysis import settings

def get_logger(domain, today=datetime.datetime.now()):
    # 基于logging模块的工具方法

    path = './../log/' + settings.BOT_NAME + '/' + domain + '/{}{}{}/'.format(today.year, today.month, today.day)
    if not os.path.exists(path):
        os.makedirs(path)
    # 这里可以配置想要的文件名称，在path后面
    path_log = path

    my_logger = logging.getLogger(domain)
    my_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s')

    scrapy_logger = logging.getLogger('scrapy')
    scrapy_logger.setLevel(logging.WARNING)

    # 配置info级的日志输出
    handler_info = logging.FileHandler('%s_info.log' % path_log, 'a', encoding='UTF-8')
    handler_info.setLevel(logging.INFO)
    handler_info.setFormatter(formatter)
    my_logger.addHandler(handler_info)
    scrapy_logger.addHandler(handler_info)

    # 配置warning级的日志输出
    handler_warning = logging.FileHandler('%s_warning.log' % path_log, 'a', encoding='UTF-8')
    handler_warning.setLevel(logging.WARNING)
    handler_warning.setFormatter(formatter)
    my_logger.addHandler(handler_warning)
    scrapy_logger.addHandler(handler_warning)

    # 配置error级的日志输出
    handler_error = logging.FileHandler('%s_error.log' % path_log, 'a', encoding='UTF-8')
    handler_error.setLevel(logging.ERROR)
    handler_error.setFormatter(formatter)
    my_logger.addHandler(handler_error)
    scrapy_logger.addHandler(handler_error)

    my_logger.info('Get my_logger success !!!')

    return my_logger