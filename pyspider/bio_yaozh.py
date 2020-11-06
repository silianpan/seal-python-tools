#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/5 4:54 下午
# @Author  : silianpan
# @Site    : 药智数据爬取
# @File    : bio_yaozh.py
# @Software: PyCharm

import json
import re

import pymysql
# from fake_useragent import UserAgent
from pyspider.libs.base_handler import *

# 正则表达式
pattern_article = re.compile(u'^https://db.yaozh.com/policies/.+.html$')
pageSize = 20
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'

common_headers = {
    'Referer': 'https://db.yaozh.com/policies?p=1&pageSize=20',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'db.yaozh.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}

common_detail_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.pkulaw.cn',
    'Upgrade-Insecure-Requests': '1'
}


class Handler(BaseHandler):
    crawl_config = {}

    def __init__(self):
        self.conn = pymysql.connect(host='172.16.95.1', user='root', password='Asdf@123', port=3306,
                                    db='db-biotown-gdss')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_taskid(self, task):
        return md5string(task['url']) + json.dumps(task['fetch'].get('data', ''))

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://db.yaozh.com/policies', method='GET', params={'p': 1, 'pageSize': pageSize},
                   save={'p': 1}, validate_cert=False,
                   callback=self.index_page, user_agent=userAgent)

    @config(age=5 * 24 * 60 * 60)
    def index_page(self, response):
        current_index = response.save['p']
        page_size = response.doc('div[data-widget="dbPagination"]').attr('data-max-page')
        if 1 <= current_index < int(page_size):
            self.crawl('https://db.yaozh.com/policies', method='GET',
                       params={'p': current_index + 1, 'pageSize': pageSize},
                       save={'p': current_index + 1}, validate_cert=False,
                       callback=self.index_page, user_agent=userAgent)
        # 逐条处理
        self.item_page(response)

    def item_page(self, response):
        # ua = UserAgent()
        for each in response.doc('a[href^="http"]').items():
            if re.match(pattern_article, each.attr.href):
                title = each.text().strip()
                self.crawl(each.attr.href, validate_cert=False, callback=self.detail_page, user_agent=userAgent)

    @config(priority=2)
    def detail_page(self, response):
        one = response.doc('.detail-main > .manual')
        title = one('.title').text().strip()
        con_list = one('.content').items()
        ret = {}
        for td in con_list:
            strong = td('span').text()
            if strong is not None:
                strong = strong.strip().replace(' ', '')
                if u'发布部门' in strong:
                    td.children().remove()
                    ret['pub_dept'] = td.text().strip()
                elif u'发文字号' in strong:
                    td.children().remove()
                    ret['pub_no'] = td.text().strip()
                elif u'效力级别' in strong:
                    td.children().remove()
                    ret['force_level'] = td.text().strip()
                elif u'发布日期' in strong:
                    td.children().remove()
                    ret['pub_date'] = td.text().strip()
                elif u'实施日期' in strong:
                    td.children().remove()
                    ret['impl_date'] = td.text().strip()
                elif u'时效性' in strong:
                    td.children().remove()
                    ret['time_valid'] = td.text().strip()

        ret['url'] = response.url
        ret['title'] = title
        ret['content'] = one.html().strip()

        self.save_to_mysql(ret)
        return ret

    # 保存到mysql
    def save_to_mysql(self, ret):
        insert_sql = """
        INSERT INTO spider_yaozh(url, title, content, pub_dept, pub_no, pub_date, impl_date, force_level, time_valid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_sql, (
                ret.get('url', ''), ret.get('title', ''), ret.get('content', ''),
                ret.get('pub_dept', ''), ret.get('pub_no', ''), ret.get('pub_date', ''),
                ret.get('impl_date', ''), ret.get('force_level', ''), ret.get('time_valid', '')))
            self.conn.commit()
        except pymysql.err.IntegrityError:
            print('Repeat Key')
