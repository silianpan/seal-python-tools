#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-11-16 19:56:43
# @Author  : silianpan
# @Site    : http://www.ibiolake.com/光谷生物城-行业资讯
# @File    : ibiolake_industry_info.py
# @Software: PyCharm

import json
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymysql
from pyspider.libs.base_handler import *

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
pattern_article = re.compile(u'^http://www.ibiolake.com/bioWeb/industryInformation/allowAccess/toIndustryInformationDetail\?id=.+$')

start_url_prefix = 'http://www.ibiolake.com/bioWeb/industryInformation/allowAccess/toIndustryInformationList'
max_page = 99


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
        # 开始爬取列表
        m_params = {'page': 1, 'rows': 10}
        self.crawl(start_url_prefix, params=m_params, save=m_params,
                   validate_cert=False, method='GET', callback=self.next_page, user_agent=userAgent)

    @config(age=5 * 24 * 60 * 60)
    def next_page(self, response):
        # 爬取详细文章
        self.item_page(response)
        # 继续爬取列表
        page = int(response.save['page'])
        if page < max_page:
            new_params = response.save
            new_params['page'] = page + 1
            self.crawl(start_url_prefix, params=new_params, save=new_params,
                       validate_cert=False, method='GET', callback=self.next_page, user_agent=userAgent)

    def item_page(self, response):
        boxs = response.doc('.talent_box').items()
        for box in boxs:
            thumbnail = box('img').attr('src')
            art_href = box('ul > li > font > a').attr('href')
            self.crawl(art_href, validate_cert=False, save={'thumbnail': thumbnail}, callback=self.detail_page, user_agent=userAgent)
        # for each in response.doc('a[href^="http"]').items():
        #     if re.match(pattern_article, each.attr.href):
        #         self.crawl(each.attr.href, validate_cert=False, callback=self.detail_page, user_agent=userAgent)

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.talent_box > p > font > span').text().strip()
        alls = response.doc('.talent_box > p:last-child').text().strip()
        pub_date = ''
        source = ''
        click_num = ''
        if alls is not None:
            ss = alls.split(u'\xa0')
            for si in ss:
                if u'发布时间' in si:
                    pub_date = si.split('：')[1].strip()
                elif u'来源' in si:
                    source = si.split('：')[1].strip()
                elif u'浏览次数' in si:
                    click_num = si.split('：')[1].strip()
        content = response.doc('.form-group').html().strip()
        ret = {
            'url': response.url,
            'title': title,
            'content': content.replace(u'\xa0', '').replace(u'\t', '').replace(u'\n', '').replace(u'\u2002', '').replace(u'\u3000', ''),
            'pub_date': pub_date,
            'source': source,
            'click_num': click_num,
            'category1': u'行业资讯',
            'thumbnail': response.save['thumbnail']
        }
        self.save_to_mysql(ret)
        return ret

    # 保存数据到数据库
    def save_to_mysql(self, ret):
        insert_sql = """
        INSERT INTO spider_ibiolake_law(url, title, content, pub_date, source, click_num, category1, thumbnail) values(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_sql, (
                ret.get('url', ''), ret.get('title', ''), ret.get('content', ''),
                ret.get('pub_date', ''), ret.get('source', ''), ret.get('click_num', ''),
                ret.get('category1', ''), ret.get('thumbnail', '')))
            self.conn.commit()
        except pymysql.err.IntegrityError:
            print('Repeat Key')
