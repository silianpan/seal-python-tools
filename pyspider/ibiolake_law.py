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

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
pattern_article = re.compile(u'^http://www.ibiolake.com/bioWeb/news/allowAccess/getNewsById\?id=.+$')

start_url_prefix = 'http://www.ibiolake.com/bioWeb/news/allowAccess/getNewsList'
# 分类爬取
start_urls = [
    {'newstype': 1, 'category2': u'国家政策', 'max_page': 76},
    {'newstype': 2, 'category2': u'省市政策', 'max_page': 27},
    {'newstype': 3, 'category2': u'东湖高新区政策', 'max_page': 5}
]


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
        for start_url in start_urls:
            # 开始爬取列表
            m_params = {'newstype': start_url['newstype'], 'page': 1, 'rows': 10, 'category2': start_url['category2'],
                        'max_page': start_url['max_page']}
            self.next_page(m_params)

    def next_page(self, m_params):
        # 爬取详细文章
        self.crawl(start_url_prefix, params=m_params, save=m_params,
                   validate_cert=False, method='GET', callback=self.item_page, user_agent=userAgent)
        # 继续爬取列表
        max_page = int(m_params['max_page'])
        page = int(m_params['page'])
        if page <= max_page:
            new_params = m_params.copy()
            new_params['page'] = page + 1
            self.crawl(start_url_prefix, params=new_params, save=new_params,
                       validate_cert=False, method='GET', callback=self.next_page, user_agent=userAgent)

    @config(age=5 * 24 * 60 * 60)
    def item_page(self, response):
        for each in response.doc('a[href]').items():
            if re.match(pattern_article, each.attr.href):
                self.crawl(each.attr.href, validate_cert=False, save={'category2': response.save['category2']},
                           callback=self.detail_page, user_agent=userAgent)

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
            'content': content.replace(u'\xa0', '').replace(u'\t', '').replace(u'\n', '').replace(u'\u2002', '').replace(u'\u3000', ''),
            'pub_date': pub_date,
            'source': source,
            'click_num': click_num,
            'category1': u'政策法规',
            'category2': response.save['category2']
        }
        self.save_to_mysql(ret)
        return ret

    # 保存数据到数据库
    def save_to_mysql(self, ret):
        insert_sql = """
        INSERT INTO spider_ibiolake_law(url, title, content, pub_date, source, click_num, category1, category2) values(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_sql, (
                ret.get('url', ''), ret.get('title', ''), ret.get('content', ''),
                ret.get('pub_date', ''), ret.get('source', ''), ret.get('click_num', ''),
                ret.get('category1', ''), ret.get('category2', '')))
            self.conn.commit()
        except pymysql.err.IntegrityError:
            print('Repeat Key')
