#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-27
# @Author  : silianpan
# @Site    : 北极星-资讯
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
from urllib.parse import urlparse


class Handler(BaseHandler):
    crawl_config = {
        'connect_timeout': 600,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }
    }

    def __init__(self):
        self.spider_config = {
            "source_url": 'https://news.bjx.com.cn',
            'urls': [
                {'url': '/yw', 'classify': 'yw', 'classify_name': u'要闻'},
            ],
            'db': {
                'host': '39.98.39.58',
                'user': 'root',
                'password': 'Asdf@123',
                'port': 3306,
                'dbname': 'smartpower-spider',
                'table_name': 'bjx_zx'
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
                      validate_cert=False, method='GET', callback=self.next_page,
                      user_agent=UserAgent().random)

    @config(age=10 * 24 * 60 * 60)
    def next_page(self, response):
        # 爬取详细文章
        self.item_page(response)
        pageCount = response.doc('.cc-paging > a:nth-last-child(2)').text().strip()
        for i in range(2, int(pageCount) + 1):
            self.crawl(response.url + '/' + str(i) + '/',
                       save={'classify': response.save['classify'], 'classify_name': response.save['classify_name']},
                       validate_cert=False, method='GET', callback=self.item_page,
                       user_agent=UserAgent().random)

    def item_page(self, response):
        boxs = response.doc('ul > li').items()
        for box in boxs:
            art_href = box('a').attr('href')
            art_title = box('a').attr('title')
            pub_date = box('span').text().strip()
            self.crawl(art_href, validate_cert=False,
                       save={'pub_date': pub_date, 'title': art_title, 'classify': response.save['classify'],
                             'classify_name': response.save['classify_name']}, callback=self.detail_page,
                             user_agent=UserAgent().random)

    @config(priority=2)
    def detail_page(self, response):
        content = response.doc('.cc-article').html().strip()
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

    # def get_proxy_list(self):
    #     return requests.get('http://webapi.http.zhimacangku.com/getip?neek=9e2a270f&num=10&type=2&time=4&pro=0&city=0&yys=0&port=1&pack=0&ts=1&ys=0&cs=0&lb=1&sb=&pb=4&mr=3&regions=&cf=0').json()
    
    # def get_random_proxy(self):
    #     if self.proxy_list and self.proxy_list.get('code') == 0:
    #         proxy_items = self.proxy_list.get('data')
    #         for item in proxy_items:
    #             if not self.is_expired(item.get('expire_time')):
    #                 return item.get('ip') + ':' + str(item.get('port'))
    #     self.proxy_list = self.get_proxy_list()
    #     return self.get_random_proxy()
    
    # def is_expired(self, dt):
    #     """
    #     判断时间是否过期
    #     :param dt:日期字符串
    #     :return:True or False
    #     """
    #     if isinstance(dt, str):
    #         dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    #         return datetime.now() > dt
    # def update_proxy(self):
    #     """
    #     重新通过api获取代理，更新代理
    #     """
    #     # 重新通过api获取代理
    #     self.proxy_list = self.get_proxy_list()
    #     new_proxy = self.get_random_proxy()
    #     return new_proxy
