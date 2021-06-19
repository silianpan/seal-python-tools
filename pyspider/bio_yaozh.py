#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/5 4:54 下午
# @Author  : silianpan
# @Site    : 药智数据爬取
# @File    : bio_yaozh.py
# @Software: PyCharm

import calendar
import datetime
import json
import os
import pathlib
import re
import time
from urllib.parse import urlparse

import pymysql
from fake_useragent import UserAgent
from pyspider.libs.base_handler import *

# 正则表达式
pattern_article = re.compile(u'^https://db.yaozh.com/policies/.+.html$')
start_url = 'https://db.yaozh.com/policies'
start_params = {
    'p': 1,
    'pageSize': 20,
    'policies_force': '全部',
    'policies_source': '全部',
    'policies_zhuangtai': '全部'
}


# userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'

def get_time_range_list(startdate, enddate):
    """
    获取时间参数列表
    :param startdate: 起始月初时间 --> str
    :param enddate: 结束时间 --> str
    :return: date_range_list -->list
    """
    date_range_list = []
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    while 1:
        next_month = startdate + datetime.timedelta(days=calendar.monthrange(startdate.year, startdate.month)[1])
        month_end = next_month - datetime.timedelta(days=1)
        if month_end < enddate:
            date_range_list.append((datetime.datetime.strftime(startdate,
                                                               '%Y-%m-%d'),
                                    datetime.datetime.strftime(month_end,
                                                               '%Y-%m-%d')))
            startdate = next_month
        else:
            return date_range_list


class Handler(BaseHandler):
    crawl_config = {}

    def __init__(self):
        self.conn = pymysql.connect(host='172.21.242.10', user='root', password='Asdf@123', port=3306,
                                    db='db-biotown-policy')
        self.cursor = self.conn.cursor()
        self.month_ranges = get_time_range_list('2000-01-01', '2021-01-01')

    def __del__(self):
        self.conn.close()

    def get_taskid(self, task):
        return md5string(task['url']) + json.dumps(task['fetch'].get('data', ''))

    @every(minutes=24 * 60)
    def on_start(self):
        for month_range in self.month_ranges:
            m_params = dict(**start_params, **{'policies_approvaldatestr': month_range[0],
                                               'policies_approvaldateend': month_range[1]})
            self.crawl(start_url, method='GET',
                       params=m_params,
                       save=m_params,
                       validate_cert=False,
                       callback=self.index_page, user_agent=UserAgent().random)

    @config(age=5 * 24 * 60 * 60)
    def index_page(self, response):
        current_index = response.save['p']
        max_page_size = response.doc('div[data-widget="dbPagination"]').attr('data-max-page')
        if 1 <= current_index < int(max_page_size):
            m_params = dict(**response.save, **{'p': current_index + 1})
            self.crawl(start_url, method='GET',
                       params=m_params,
                       save=m_params, validate_cert=False,
                       callback=self.index_page, user_agent=UserAgent().random)
        # 逐条处理
        self.item_page(response)

    def item_page(self, response):
        ua = UserAgent()
        for each in response.doc('a[href^="http"]').items():
            if re.match(pattern_article, each.attr.href):
                # title = each.text().strip()
                self.crawl(each.attr.href, validate_cert=False, callback=self.detail_page, user_agent=ua.random)

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

        json_file = self.build_local_json_file(response);
        ret['json_url'] = json_file['json_url']
        self.save_to_json(json_file['file_path'], ret)

        self.save_to_mysql(ret)
        return ret

    # 构建本地存储json文件
    def build_local_json_file(self, response):
        pr = urlparse(response.url)
        partitions = pr.path.partition('.')
        out_dir = '/home/tmp/output/'
        # db.yaozh.com => dbyaozhcom
        source = pr.netloc.replace('.', '')
        # 日期：2020-11-12
        now_day = time.strftime('%Y-%m-%d', time.localtime())
        # /Users/hsc/CodeWorkSpace/projects/tianfu-bio-town/code/biotown-parent/spider/dbyaozhcom
        p_dir = os.path.join(out_dir, "{0}/{1}".format(source, now_day))
        # /policies/6247.json
        file_name = partitions[0] + '.json'
        return {
            # dbyaozhcom/2020-11-12/policies/6247.json
            "json_url": "{0}/{1}{2}".format(source, now_day, file_name),
            # /Users/hsc/CodeWorkSpace/projects/tianfu-bio-town/code/biotown-parent/spider/dbyaozhcom/policies/6247.json
            "file_path": p_dir + file_name
        }

    # 存储到文件中
    def save_to_json(self, filePath, data):
        dir_name = os.path.dirname(filePath)
        pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)
        json_str = json.dumps(data, ensure_ascii=False)
        with open(filePath, 'w', encoding='utf-8') as json_file:
            json_file.write(json_str)

    # 保存到mysql
    def save_to_mysql(self, ret):
        insert_sql = """
        INSERT INTO spider_bio_policy(url, title, content, pub_dept, pub_no, pub_date, impl_date, force_level, time_valid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_sql, (
                ret.get('url', ''), ret.get('title', ''), ret.get('content', ''),
                ret.get('pub_dept', ''), ret.get('pub_no', ''), ret.get('pub_date', ''),
                ret.get('impl_date', ''), ret.get('force_level', ''), ret.get('time_valid', '')))
            self.conn.commit()
        except pymysql.err.IntegrityError:
            print('Repeat Key')
