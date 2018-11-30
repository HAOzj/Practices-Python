# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on NOV 30, 2018

@author: woshihaozhaojun@sina.com
"""
import pymysql

class Mysql:
    def __init__(self, db_host, user, password, database, port):
        self.db = pymysql.connect(host=db_host,
                                  user=user,
                                  passwd=password,
                                  db=database,
                                  port=port,
                                  charset="utf8")

    def query(self, sql):
        """
        query
        """
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print sql
            raise e

    def query__SSCursor(self, sql):
        """
        query
        """
        try:
            with self.db.cursor(pymysql.cursors.SSCursor) as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print sql
            raise e

    def execute(self, sql):
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
                self.db.commit()
        except Exception as e:
            print sql
            raise e


    def close(self):
        """
        close connection
        """
        self.db.close()

