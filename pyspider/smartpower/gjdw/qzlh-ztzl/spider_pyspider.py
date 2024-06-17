#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-27
# @Author  : silianpan
# @Site    : 国家电网-旗帜领航-专题专栏
# @File    : spider_news.py
# @Software: PyCharm

import json
import os
import time

import pathlib
import pymysql
from pyspider.libs.base_handler import *
from urllib.parse import urlparse


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
            'Cache-Control': 'max-age=0',
            'Cookie': 'Rq9ZlcGkVvC3S=60krow3RM27oI7EaMaEmYqgtES_ByaGvNdoSaqdM9lZu6HFHaZjMQObOi2QdoU0P7Omq_vUwFFYWg9CdBV4VLqoq; Rq9ZlcGkVvC3T=0U.O6fCGCPsQgwLAwxp05_XlncBhTCh7UqqZI85RGO5jcDzxbEdRrpf9fMeQMrp5OKXGubspWZtbIlcNY1xApkOGlI7LtvVssfjKenC0WprLPVPspoD8cG1QcAeHeHQ0pgKJNwGTxbm.0ictrj1b0DnYiBuYER_uehzr3xfr_k1CrYin3gHntxZl2btoB_DftC_fSgln5YrSOhrZq0endnMweK0dgM6.F8.wxGPER8FIY4hIiJuWM6Z8z27XhGR8ZBT1CH3o4gAqO6b1YoVBw1XaxORS092d74PKgC2QEbYE3VTRHu5l2itv7ITZ2eztIFy7Bk1onU0jMgFaFw_VraUnEF8U1qIRS_54esepy2xSJx9LD2iCjQfA71ZCg7zFkCaFVxK5SnNIk2cDVzGYRAHCpwiMMqv.7ZgjSKK8JPLl',
            'Host': 'www.sgcc.com.cn',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.sgcc.com.cn/html/sgcc/col2022121491/column_2022121491_1.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }
    }

    def __init__(self):
        self.spider_config = {
            "source_url": 'http://www.sgcc.com.cn/html/sgcc',
            'urls': [
                {'url': '/col2022121491/column_2022121491_1.shtml', 'classify': 'zyjh', 'classify_name': u'重要讲话'},
                {'url': '/col2022121473/column_2022121473_1.shtml#here', 'classify': 'xxqg', 'classify_name': u'学习强国'}
            ],
            'db': {
                'host': '39.98.39.58',
                'user': 'root',
                'password': 'Asdf@123',
                'port': 3306,
                'dbname': 'smartpower-spider',
                'table_name': 'qzlh_ztzl'
            },
            # 存储到本地的文件夹
            'file': {
                'out_dir': '/home/tmp/output/',
            }
        }
        self.conn = pymysql.connect(host=self.spider_config['db']['host'], user=self.spider_config['db']['user'],
                                    password=self.spider_config['db']['password'],
                                    port=self.spider_config['db']['port'],
                                    db=self.spider_config['db']['dbname'])
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_taskid(self, task):
        return md5string(task['url']) + json.dumps(task['fetch'].get('data', ''))

    @every(minutes=24 * 60)
    def on_start(self):
       for item in self.spider_config['urls']:
           self.crawl(self.spider_config['source_url'] + item['url'], fetch_type="js",
                      validate_cert=False, method='GET', callback=self.next_page)

    @config(age=10 * 24 * 60 * 60)
    def next_page(self, response):
        # 爬取详细文章
        self.item_page(response)

    def item_page(self, response):
        boxs = response.doc('.newslist > li').items()
        for box in boxs:
            art_href = box('a').attr('href')
            art_title = box('a').attr('title')
            pub_date = box('i').text().strip()
            self.crawl(art_href, validate_cert=False,
                       save={'pub_date': pub_date, 'title': art_title}, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.doc('.mbox').html().strip()
        obj = {
           'main': {
               'content': content,
               'filename': response.save['title'],
           },
           'medias': []
        }
        ret = {
            'id': md5string(response.url),
            'json': json.dumps(obj, ensure_ascii=False,)
        }
        self.save_to_mysql(self.spider_config['db']['table_name'], ret)
        return ret

    # 自动构建sql
    def build_insert_sql(self, table_name, fields):
        place_holder = ['%s'] * len(fields)
        sql = "INSERT INTO %s (%s) values(%s)" % (
            table_name, ','.join(['`%s`'] * len(fields)) % tuple(fields), ','.join(place_holder))
        return sql

    # 保存到mysql
    def save_to_mysql(self, table_name, data):
        fields = [str(f) for f, v in data.items()]
        values = []
        for f, v in data.items():
            if isinstance(v, str) is False:
                values.append(json.dumps(v, ensure_ascii=False));
            else:
                values.append(v)
        insert_sql = self.build_insert_sql(table_name, fields)
        try:
            # 执行SQL语句
            self.cursor.execute(insert_sql, tuple(values))
            # 提交到数据库执行
            self.conn.commit()
        except pymysql.err.IntegrityError:
            # 发生错误时回滚
            self.conn.rollback()
