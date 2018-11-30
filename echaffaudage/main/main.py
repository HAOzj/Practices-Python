#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on NOV 30, 2018

@author : woshihaozhaojun@sina.com
'''


import os
import sys
import time
import datetime
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import (
    print_run_time, get_updir_path
)
from module import xixi
import warnings
warnings.filterwarnings("ignore")

class Haha():
    def __init__(self, conf_path):
        self.conf_path = conf_path


    @print_run_time
    def all_process(self, statdate):
        '''
        '''
        houhou = xixi.Xixi(self.conf_path)
        houhou.xxmethod()
        houhou.stop_connection()

if __name__ == "__main__":
    print datetime.datetime.now()
    optparser = OptionParser()
    optparser.add_option('-c', '--conf_path', dest='conf_path', help='参数路径',
                         type="string", default="config/config.yaml")
    (options, args) = optparser.parse_args()
    start_time = time.time()
    haha = Haha(options.conf_path)
    haha.all_process(options.num)