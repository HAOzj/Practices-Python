# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on NOV 30, 2018

@author: woshihaozhaojun@sina.com
"""
from pyhive import hive

class HiveClient():
    def __init__(self, db_host, database, port=10000, authMechanism="KERBEROS"):
        """
        create connection to hive server2
        """
        self.conn = hive.connect(host=db_host,
                                 port=port,
                                 auth = authMechanism,
                                 kerberos_service_name = "hive",
                                 database=database)
        print "-----succeed in connecting hive-----"

    def query(self, hql):
        """
        query
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(hql)
                return cursor.fetchall()
        except Exception as e:
            print hql
            raise e 

    def close(self):
        """
        close connection
        """
        self.conn.close()

