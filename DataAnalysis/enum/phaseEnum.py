#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 15:12
# @Author  : hydria
# @Site    : 
# @File    : phaseEnum.py
# @Software: PyCharm

from enum import Enum

class phase(Enum):
    # 融资轮次枚举类

    SEED = '种子轮'
    ANGEL = '天使轮'
    PRE_A = 'Pre-A轮'
    A = 'A轮'
    A_PLUS = 'A+轮'
    PRE_B = 'Pre-B轮'
    B = 'B轮'
    B_PLUS = 'B+轮'
    C = 'C轮'
    C_PLUS = 'C+轮'
    D = 'D轮'
    E = 'E轮'
    INFORMAL = '战略投资'
    PRIVATE_REPLACEMENT = '定增'
    AFTER_IPO = '上市后'
    IPO = 'IPO'
    PRE_IPO = 'Pre-IPO'
    ACQUIRED = '并购'
    NEEQ = '新三板'