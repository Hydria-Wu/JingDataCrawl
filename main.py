#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/10 18:38
# @Author  : hydria
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jingData"])



# scrapy crawl jingData -s JOBDIR=job_info/001