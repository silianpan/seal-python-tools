#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-11-16 19:56:43
# @Author  : silianpan
# @Site    : http://www.ibiolake.com/光谷生物城政策法规
# @File    : ibiolake_law.py
# @Software: PyCharm

import json
import re

import pymysql
from pyspider.libs.base_handler import *

pattern_article = re.compile(u'^http://www.ibiolake.com/bioWeb/news/allowAccess/getNewsById\?id=.+$')
url_prefix = 'http://www.ibiolake.com'
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'


class Handler(BaseHandler):
    crawl_config = {}

    def __init__(self):
        self.conn = pymysql.connect(host='172.16.95.1', user='root', password='Asdf@123', port=3306,
                                    db='db-biotown-others')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_taskid(self, task):
        return md5string(task['url']) + json.dumps(task['fetch'].get('data', ''))

    @every(minutes=24 * 60)
    def on_start(self):
        m_params = {'newstype': 1, 'page': 1, 'rows': 10}
        self.crawl(url_prefix + '/bioWeb/news/allowAccess/getNewsList',
                   params=m_params,
                   save=m_params,
                   validate_cert=False, method='GET', callback=self.item_page, user_agent=userAgent)

    @config(age=5 * 24 * 60 * 60)
    def item_page(self, response):
        for each in response.doc('a[href]').items():
            if re.match(pattern_article, each.attr.href):
                self.crawl(each.attr.href, validate_cert=False, callback=self.detail_page, user_agent=userAgent)

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.talent_box > .all_title > b').text().strip()
        alls = response.doc('.talent_box > .all_title_time').text().strip()
        pub_date = ''
        source = ''
        click_num = ''
        if alls is not None:
            ss = alls.split('\xa0')
            for si in ss:
                if u'发布时间' in si:
                    pub_date = si.split('：')[1].strip()
                elif u'来源' in si:
                    source = si.split('：')[1].strip()
                elif u'点击' in si:
                    click_num = si.split('：')[1].strip()
        content = response.doc('.talent_box > .form-group').html().strip()
        ret = {
            'url': response.url,
            'title': title,
            'content': content.replace('\xa0', '&nbsp;').replace('\t', '').replace('\n', ''),
            'pub_date': pub_date,
            'source': source,
            'click_num': click_num
        }
        self.save_to_mysql(ret)
        return ret

    # 保存数据到数据库
    def save_to_mysql(self, ret):
        insert_sql = """
        INSERT INTO spider_ibiolake_law(url, title, content, pub_date, source, click_num) values(%s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_sql, (
                ret.get('url', ''), ret.get('title', ''), ret.get('content', ''),
                ret.get('pub_date', ''), ret.get('source', ''), ret.get('click_num', '')))
            self.conn.commit()
        except pymysql.err.IntegrityError:
            print('Repeat Key')
