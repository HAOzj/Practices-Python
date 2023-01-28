# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on OCT 22, 2018
@author: woshihaozhaojun@sina.com
"""
import os
import time
import json
import datetime

def get_updir_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_upupdir_path():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_dir_path():
    return os.path.abspath(os.path.dirname(__file__))

def get_dict_from_json(filename):
    if os.path.isfile(filename):
        return json.load( open(filename, "r"), encoding="utf8")
    else :
        print filename, " doesn't exist"
        return dict()

def get_date(num = 1 ):
    ''' 得到{num}天前的日期,返回yyyy-mm-dd的形式

    Args:
        num(int) :- 默认为1,要得到的日期距离今天的天数
    Returns:
        yyyy-mm-dd形式的日期字符串
    '''
    yesterday = datetime.datetime.now().date() - datetime.timedelta( days = num)
    year = yesterday.year
    month = yesterday.month
    day = yesterday.day

    if month < 10 :
        month = "0{}".format(month)
    if day < 10 :
        day = "0{}".format(day)

    return "{}-{}-{}".format(year, month, day)


def print_run_time(func):
    ''' 计算时间函数
    '''
    def wrapper(*args, **kw):
        local_time = time.time()
        res = func(*args, **kw)
        print('Current function : {function}, time used : {temps}'.format(
            function=func.__name__, temps=time.time() - local_time))
        return res
    return wrapper


import unicodedata
import string
def shave_marks(txt):
    """去掉全部变音符号"""
    norm_txt = unicodedata.normalize('NFD', txt)
    shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)