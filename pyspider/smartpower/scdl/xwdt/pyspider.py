#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-27
# @Author  : silianpan
# @Site    : 四川电力-新闻动态
# @File    : scdl_xwdt.py
# @Software: PyCharm

import json
import os
import time
import base64

import pathlib
import pymysql
from pyspider.libs.base_handler import *
from urllib.parse import urlparse


class Handler(BaseHandler):
    crawl_config = {
        'connect_timeout': 600,
        'headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
            'Cache-Control': 'max-age=0',
            'Host': 'www.sc.sgcc.com.cn',
            'If-None-Match': 'W/"665ed489-4f10"',
            'Referer': 'https://www.sc.sgcc.com.cn/html/main/col3/column_3_1.html',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        }
    }

    def __init__(self):
        self.spider_config = {
            "source_url": 'https://www.sc.sgcc.com.cn/html/main',
            'urls': [
                {'url': '/col8/column_8_1.html', 'classify': 'gsyw', 'classify_name': u'公司要闻'},
                {'url': '/col9/column_9_1.html', 'classify': 'zbdt', 'classify_name': u'总部动态'},
                {'url': '/col81/column_81_1.html', 'classify': 'yxdt', 'classify_name': u'一线动态'},
                {'url': '/col37/column_37_1.html', 'classify': 'mtjj', 'classify_name': u'媒体聚焦'},
            ],
            'db': {
                'host': '39.98.39.58',
                'user': 'root',
                'password': 'Asdf@123',
                'port': 3306,
                'dbname': 'smartpower-spider',
                'table_name': 'scdl_xwdt'
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
           self.crawl(self.spider_config['source_url'] + item['url'], save={'classify': item['classify'], 'classify_name': item['classify_name']},
                      validate_cert=False, method='GET', callback=self.next_page)

    @config(age=10 * 24 * 60 * 60)
    def next_page(self, response):
        # 爬取详细文章
        self.item_page(response)
        pageCount = response.doc('.pagenav > form > #pagenavpagecount > b').text().strip()
        for i in range(2, int(pageCount) + 1):
            self.crawl(response.url.replace('1.html', str(i) + '.html'),
                       save={'classify': response.save['classify'], 'classify_name': response.save['classify_name']},
                       validate_cert=False, method='GET', callback=self.item_page)

    def item_page(self, response):
        boxs = response.doc('ul.list > li').items()
        for box in boxs:
            art_href = box('a').attr('href')
            if 'portal.sc.sgcc.com.cn' not in art_href:
                art_title = box('a').text().strip()
                pub_date = box('span').text().strip()
                self.crawl(art_href, validate_cert=False,
                           save={'pub_date': pub_date, 'title': art_title, 'classify': response.save['classify'],
                                 'classify_name': response.save['classify_name']}, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.doc('.txtcon').html().strip()
        # b64encode函数的参数为byte类型，所以必须先转码
        contentBytesString = content.encode('utf-8')
        obj = {
           'main': {
               'content': str(base64.b64encode(contentBytesString), 'utf-8'),
               'filename': response.save['title'],
           },
           'medias': []
        }
        ret = {
            'id': md5string(response.url),
            'url': response.url,
            'classify': response.save['classify'],
            'classify_name': response.save['classify_name'],
            'title': response.save['title'],
            'pub_date': response.save['pub_date'],
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
