#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/5 4:54 下午
# @Author  : silianpan
# @Site    : 新浪医药新闻爬取
# @File    : bio_med_sina.py
# @Software: PyCharm

import json
import re

import pymysql
# from fake_useragent import UserAgent
from pyspider.libs.base_handler import *

pattern_article = re.compile(u'^https://med.sina.com/article_detail_.+.html$')
url_prefix = 'https://med.sina.com/'
urls = [
    {'url': 'article_list_103_2_%s_3554.html', 'max_page': 3600},
    {'url': 'feature_list_322_%s_70.html', 'max_page': 80},
    {'url': 'feature_list_284_%s_107.html', 'max_page': 110},
    {'url': 'feature_list_1341_%s_33.html', 'max_page': 40}
]

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'


class Handler(BaseHandler):
    crawl_config = {}

    def __init__(self):
        self.conn = pymysql.connect(host='172.16.95.1', user='root', password='Asdf@123', port=3306,
                                    db='db-biotown-realtime-info')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_taskid(self, task):
        return md5string(task['url']) + json.dumps(task['fetch'].get('data', ''))

    @every(minutes=24 * 60)
    def on_start(self):
        for item in urls:
            for i in range(1, item['max_page']):
                crawl_url = url_prefix + str(item['url'] % i)
                self.crawl(crawl_url, validate_cert=False, method='GET', callback=self.item_page, user_agent=userAgent)

    @config(age=5 * 24 * 60 * 60)
    def item_page(self, response):
        # ua = UserAgent()
        for each in response.doc('a[href^="http"]').items():
            if re.match(pattern_article, each.attr.href):
                self.crawl(each.attr.href, validate_cert=False, callback=self.detail_page, user_agent=userAgent)

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.news > h1.news-title').text().strip()
        source = response.doc('.news > .wz-tbbox > .wz-zuthorname > em').text()
        if source is None or source == '' or source.strip() == '':
            source = response.doc('.news > .wz-tbbox > .wz-zuthorname').text().strip()
            if u'来源' in source:
                source = source.split(u'：')[1]
        source = source.strip()
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

    # 保存数据到数据库
    def save_to_mysql(self, ret):
        insert_sql = """
        INSERT INTO spider_realtime_info(url, title, content, pub_date, source) values(%s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_sql, (
                ret.get('url', ''), ret.get('title', ''), ret.get('content', ''),
                ret.get('pub_date', ''), ret.get('source', '')))
            self.conn.commit()
        except pymysql.err.IntegrityError:
            print('Repeat Key')
