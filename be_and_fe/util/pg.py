# -*- coding: utf8 -*-
"""
Created on Sep 30, 2024

@author: woshihaozhaojun@sina.com
"""
import psycopg2
import traceback
from psycopg2.extras import RealDictCursor


class Postgres(object):
    def __init__(self, conf_dict):
        self.conf_dict = conf_dict
        self.db = psycopg2.connect(**self.conf_dict)

    def execute(self, sql):
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
                self.db.commit()
        except Exception as e:
            print(sql)
            raise e

    def query(self, sql):
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(sql)
            raise e

    def close(self):
        self.db.close()