#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/13 16:33
# @Author  : hydria
# @Site    : 
# @File    : LogUtil.py
# @Software: PyCharm

import datetime, os, logging
from DataAnalysis import settings

class logs(object):

    def __init__(self, domain, today=datetime.datetime.now()):
        # 基于logging模块的工具方法

        path = './../log/' + settings.BOT_NAME + '/' + domain + '/{}{}{}/'.format(today.year, today.month, today.day)
        if not os.path.exists(path):
            os.makedirs(path)
        # 这里可以配置想要的文件名称，在path后面
        path_log = path

        my_logger = logging.getLogger(domain)
        my_logger.propagate = False
        my_logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s')

        # 配置info级的日志输出
        handler_info = logging.FileHandler('%s_info.log' % path_log, 'a', encoding='UTF-8')
        handler_info.setLevel(logging.INFO)
        handler_info.setFormatter(formatter)

        # 配置warning级的日志输出
        handler_warning = logging.FileHandler('%s_warning.log' % path_log, 'a', encoding='UTF-8')
        handler_warning.setLevel(logging.WARNING)
        handler_warning.setFormatter(formatter)

        # 配置error级的日志输出
        handler_error = logging.FileHandler('%s_error.log' % path_log, 'a', encoding='UTF-8')
        handler_error.setLevel(logging.ERROR)
        handler_error.setFormatter(formatter)

        self.handler_info = handler_info
        self.handler_warning = handler_warning
        self.handler_error = handler_error
        self.logger = my_logger

    def info(self, msg):
        self.logger.addHandler(self.handler_info)
        self.logger.info(msg)
        self.logger.removeHandler(self.handler_info)

    def warning(self, msg):
        self.logger.addHandler(self.handler_warning)
        self.logger.warning(msg)
        self.logger.removeHandler(self.handler_warning)

    def error(self, msg):
        self.logger.addHandler(self.handler_error)
        self.logger.error(msg)
        self.logger.removeHandler(self.handler_error)
