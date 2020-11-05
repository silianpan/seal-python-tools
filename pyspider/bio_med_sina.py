#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/5 6:04 下午
# @Author  : silianpan
# @Site    : 
# @File    : bio_med_sina.py
# @Software: PyCharm

import json
import re

import pymysql
from fake_useragent import UserAgent
from pyspider.libs.base_handler import *

pattern_article = re.compile(u'^https://med.sina.com/article_detail_.+.html$')

urls = [
    'https://med.sina.com/column/zonghe/',
    'https://med.sina.com/feature_322.html',
    'https://med.sina.com/feature_284.html',
    'https://med.sina.com/feature_1341.html'
]

class Handler(BaseHandler):
    crawl_config = {}

    def __init__(self):
        pass

    def __del__(self):
        pass

    def get_taskid(self, task):
        return md5string(task['url']) + json.dumps(task['fetch'].get('data', ''))

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://med.sina.com/column/zonghe/', method='GET', callback=self.index_page, user_agent=UserAgent().random)

    @config(age=5 * 24 * 60 * 60)
    def index_page(self, response):
        next_page = response.doc('a.clickmore')
        if next_page is not None:
            sign = next_page.attr('sign')
            if sign is not None:
                signs = sign.strip().split('_')
                print(signs[0], signs[1], signs[2], signs[3])
                print(int(signs[2]) + 1)
                next_sign = int(signs[2]) + 1
                next_url_prefix = 'https://med.sina.com/article_list_'
                next_url = next_url_prefix + signs[0] + '_' + signs[1] + '_' + next_sign + '_' + signs[3] + '.html'
                print(next_url)
                self.crawl(next_url, method='GET', callback=self.index_page, user_agent=UserAgent().random)
        # 逐条提取
        self.item_page(response)

    def item_page(self, response):
        ua = UserAgent()
        for each in response.doc('a[href^="http"]').items():
            if re.match(pattern_article, each.attr.href):
                # title = each.text().strip()
                self.crawl(each.attr.href, callback=self.detail_page, user_agent=ua.random)

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.news > h1.news-title').text().strip()
        source = response.doc('.news > .wz-tbbox > .wz-zuthorname > em').text().strip()
        pub_date = response.doc('.news > .wz-tbbox > .wz-fbtime').text().strip()
        content = response.doc('.news > .textbox').html().strip()
        ret = {
            'url': response.url,
            'title': title,
            'content': content,
            'pub_date': pub_date,
            'source': source
        }
        self.save_to_mysql(ret)
        return ret

    # 保存数据库
    def save_to_mysql(self, ret):
        insert_sql = """
        INSERT INTO spider_med_sina(url, title, content, pub_date, source) values(%s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_sql, (
                ret.get('url', ''), ret.get('title', ''), ret.get('content', ''),
                ret.get('pub_date', ''), ret.get('source', '')))
            self.conn.commit()
        except pymysql.err.IntegrityError:
            print('Repeat Key')
