# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on NOV 30, 2018

@author: woshihaozhaojun@sina.com
"""
import yaml
import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (mysql, hive)
from utils.utils import print_run_time

class Xixi():
    def __init__(self, conf_path):
        self.yaml_conf_dic = yaml.load(open(conf_path, 'r'))

        self.mysql_client = mysql.Mysql(
            db_host=self.yaml_conf_dic['Mysql']['Host'],
            port=int(
                self.yaml_conf_dic['Mysql']['Port']),
            user=self.yaml_conf_dic['Mysql']['User'],
            password=self.yaml_conf_dic['Mysql']['Password'],
            database=self.yaml_conf_dic['Mysql']['Db_name'])

        self.hive_client = hive.HiveClient(
            db_host=self.yaml_conf_dic["Hive"]["Host"],
            database=self.yaml_conf_dic["Hive"]["Db_name"])

    @print_run_time
    def xxmethod(self):
        return "hello world!"

    def stop_connection(self):
        self.mysql_client.close()
