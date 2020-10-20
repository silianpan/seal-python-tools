#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/19 9:55 上午
# @Author  : silianpan
# @Site    : mysql工具
# @File    : mysql_util.py
# @Software: PyCharm

import logging

import pymysql

logger = logging.getLogger(__name__)


class MysqlUtil:
    def __init__(self, mysql_host, mysql_db, mysql_user, mysql_pwd, mysql_port=3306):
        self.is_connected = False
        try:
            self.conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_pwd, port=mysql_port,
                                        db=mysql_db)
            self.cursor = self.conn.cursor()
            self.is_connected = True
        except Exception as e:
            logger.error(e)

    # def __del__(self):
    #     self.conn.close()

    def escape(self, string):
        return '%s' % string

    def select(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(e)

    def update_sql(self, sql):
        if self.is_connected:
            try:
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                logger.error(e)

    def insert(self, tablename=None, **ret):
        if self.is_connected:
            tablename = self.escape(tablename)
            _keys = ",".join(self.escape(k) for k in ret)
            _values = ",".join(['%s', ] * len(ret))
            insert_sql = "insert into %s (%s) values (%s)" % (tablename, _keys, _values)
            try:
                self.cursor.execute(insert_sql, tuple(ret.values()))
                self.conn.commit()
            except Exception as e:
                logger.error(e)
