#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-27
# @Author  : silianpan
# @Site    : 北极星-行业-智能电网
# @File    : scdl_xwdt.py
# @Software: PyCharm

import json
import os
import time
import base64
import requests
from datetime import datetime
from fake_useragent import UserAgent

import pathlib
import pymysql
from pyspider.libs.base_handler import *
from urllib.parse import urlparse, parse_qs


class Handler(BaseHandler):
    crawl_config = {
        'connect_timeout': 600,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }
    }

    def __init__(self):
        self.spider_config = {
            "source_url": 'http://www.chinasmartgrid.com.cn',
            'urls': [
                {'url': '/NewsList.aspx', 'classify': 'yw', 'classify_name': u'要闻', 'industry': u'智能电网'},
                {'url': '/List-News?rid=112', 'classify': 'zc', 'classify_name': u'政策', 'industry': u'智能电网'},
                {'url': '/List-News?rid=119', 'classify': 'sc', 'classify_name': u'市场', 'industry': u'智能电网'},
                {'url': '/List-News?rid=131', 'classify': 'jsqy', 'classify_name': u'技术前沿', 'industry': u'智能电网'},
                {'url': '/List-Tech?rid=140', 'classify': 'jswz', 'classify_name': u'技术文章', 'industry': u'智能电网'},
                {'url': '/List-News?rid=132', 'classify': 'sj', 'classify_name': u'数据', 'industry': u'智能电网'},
                {'url': '/List-News?rid=116', 'classify': 'ft', 'classify_name': u'访谈', 'industry': u'智能电网'},
                {'url': '/List-News?rid=125', 'classify': 'pl', 'classify_name': u'评论', 'industry': u'智能电网'},
                {'url': '/List-News?rid=133', 'classify': 'bd', 'classify_name': u'报道', 'industry': u'智能电网'},
                {'url': '/List-News?rid=134', 'classify': 'gj', 'classify_name': u'国际', 'industry': u'智能电网'},
                {'url': '/List-News?rid=122', 'classify': 'cj', 'classify_name': u'财经', 'industry': u'智能电网'},
                {'url': '/List-News?rid=128', 'classify': 'hy', 'classify_name': u'会议', 'industry': u'智能电网'},
            ],
            'db': {
                'host': '39.98.39.58',
                'user': 'root',
                'password': 'Asdf@123',
                'port': 3306,
                'dbname': 'smartpower-spider',
                'table_name': 'bjx_hy'
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
           self.crawl(self.spider_config['source_url'] + item['url'], save={'classify': item['classify'], 
                                                                            'classify_name': item['classify_name'],
                                                                            'industry': item['industry']},
                      validate_cert=False, method='GET', callback=self.next_page,
                      user_agent=UserAgent().random)

    @config(age=10 * 24 * 60 * 60)
    def next_page(self, response):
        # 爬取详细文章
        self.item_page(response)
        page = self.get_url_param(response.url, 'page')

        next_obj = response.doc('.list_page > .page > a:last-child')
        next_url = next_obj.attr('href')
        next_page = self.get_url_param(next_url, 'page')
        if page is None or (next_page is not None and int(page) != int(next_page)):
            self.crawl(next_url, save={'classify': response.save['classify'], 'classify_name': response.save['classify_name'],
                                       'industry': response.save['industry']},
                       validate_cert=False, method='GET', callback=self.next_page,
                       user_agent=UserAgent().random)

    def item_page(self, response):
        boxs = response.doc('ul.list_left_ul > li').items()
        for box in boxs:
            art_href = box('a').attr('href')
            art_title = box('a').attr('title')
            pub_date = box('span').text().strip()
            self.crawl(art_href, validate_cert=False,
                       save={'pub_date': pub_date, 'title': art_title, 'classify': response.save['classify'],
                             'classify_name': response.save['classify_name'], 'industry': response.save['industry']},
                             callback=self.detail_page,
                             user_agent=UserAgent().random)

    @config(priority=2)
    def detail_page(self, response):
        content = response.doc('.list_detail').html()
        if content is None:
            content = response.doc('.content').html()
            if content is None:
                return
        content = content.strip()
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
            'industry': response.save['industry'],
            'title': response.save['title'],
            'pub_date': response.save['pub_date'],
            'content': content,
            'json': json.dumps(obj, ensure_ascii=False)
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
    
    # 获取url参数
    def get_url_param(self, url, key):
        parsed = urlparse(url)
        querys = parse_qs(parsed.query)
        if querys and (key in querys) and querys[key]:
            return querys[key][0]
        return None
