#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/19 11:13 上午
# @Author  : silianpan
# @Site    : oracle工具
# @File    : oracle_util.py
# @Software: PyCharm

import logging
import cx_Oracle

logger = logging.getLogger(__name__)
cx_Oracle.init_oracle_client(lib_dir='/Users/liupan/Downloads/Oracle11.2.0.1.0/instantclient_19_8')

class OracleUtil:
    def __init__(self, host, port, service_name, user, pwd):
        self.is_connected = False
        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_name)
        try:
            self.conn = cx_Oracle.connect(user=user, password=pwd, dsn=dsn_tns)
            self.cursor = self.conn.cursor()
            self.is_connected = True
        except Exception as e:
            logger.error(e)

    def select(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(e)
