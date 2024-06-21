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
            ':authority': 'news.bjx.com.cn',
            ':method': 'GET',
            ':scheme': 'https',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
            'Cache-Control': 'max-age=0',
            'Host': 'www.sc.sgcc.com.cn',
            'If-None-Match': 'W/"665ed489-4f10"',
            'Referer': 'https://news.bjx.com.cn/zc/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'bjx:uuid=c926b6f7-0d96-4792-925c-f32a4578e098; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22190340a8821a1f-06be3105d450a0c-26001c51-2073600-190340a8822b76%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwMzQwYTg4MjFhMWYtMDZiZTMxMDVkNDUwYTBjLTI2MDAxYzUxLTIwNzM2MDAtMTkwMzQwYTg4MjJiNzYifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; Hm_lvt_797e95e42c7a8bdc8814749cbcddd277=1718860024; bjx_mt:nonce=4823661037; Hm_lvt_a63cd5ba9dde57be0e99585c01013858=1718860130; Hm_lvt_c32964cdd0907bbd6938f89413c67dee=1718931182; Hm_lpvt_c32964cdd0907bbd6938f89413c67dee=1718931304; Hm_lvt_f00f976ac31edaff2c65030ca9707c36=1718931517; Hm_lpvt_f00f976ac31edaff2c65030ca9707c36=1718931517; Hm_lpvt_797e95e42c7a8bdc8814749cbcddd277=1718931952; Hm_lpvt_a63cd5ba9dde57be0e99585c01013858=1718931953'
        }
    }

    def __init__(self):
        self.proxy_list = self.get_proxy_list()
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
                      validate_cert=False, method='GET', callback=self.next_page, proxy='http://{proxy}'.format(proxy=self.get_random_proxy()),
                      user_agent=UserAgent().random)

    @config(age=10 * 24 * 60 * 60)
    def next_page(self, response):
        # 爬取详细文章
        self.item_page(response)
        pageCount = response.doc('.cc-paging > a:nth-last-child(2)').text().strip()
        for i in range(2, int(pageCount) + 1):
            self.crawl(response.url + '/' + str(i) + '/',
                       save={'classify': response.save['classify'], 'classify_name': response.save['classify_name']},
                       validate_cert=False, method='GET', callback=self.item_page, proxy='http://{proxy}'.format(proxy=self.get_random_proxy()),
                       user_agent=UserAgent().random)

    def item_page(self, response):
        if response.status_code in [401, 403, 599]:
            self.crawl(response.url, save={'classify': response.save['classify'], 'classify_name': response.save['classify_name']},
                       validate_cer=False, method='GET', callback=self.item_page, proxy='http://{proxy}'.format(proxy=self.update_proxy()),
                       user_agent=UserAgent().random)
        boxs = response.doc('.cc-list-content > ul > li').items()
        for box in boxs:
            art_href = box('a').attr('href')
            art_title = box('a').attr('title')
            pub_date = box('span').text().strip()
            self.crawl(art_href, validate_cert=False,
                       save={'pub_date': pub_date, 'title': art_title, 'classify': response.save['classify'],
                             'classify_name': response.save['classify_name']}, callback=self.detail_page,
                             proxy='http://{proxy}'.format(proxy=self.get_random_proxy()), user_agent=UserAgent().random)

    @config(priority=2)
    def detail_page(self, response):
        if response.status_code in [401, 403, 599]:
            self.crawl(response.url, save={'classify': response.save['classify'], 'classify_name': response.save['classify_name'],
                                           'title': response.save['title'], 'pub_date': response.save['pub_date']},
                       validate_cer=False, method='GET', callback=self.item_page, proxy='http://{proxy}'.format(proxy=self.update_proxy()),
                       user_agent=UserAgent().random)
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

    def get_proxy_list(self):
        return requests.get('http://webapi.http.zhimacangku.com/getip?neek=9e2a270f&num=10&type=2&time=4&pro=0&city=0&yys=0&port=1&pack=0&ts=1&ys=0&cs=0&lb=1&sb=&pb=4&mr=3&regions=&cf=0').json()
    
    def get_random_proxy(self):
        if self.proxy_list and self.proxy_list.get('code') == 0:
            proxy_items = self.proxy_list.get('data')
            for item in proxy_items:
                if not self.is_expired(item.get('expire_time')):
                    return item.get('ip') + ':' + str(item.get('port'))
        self.proxy_list = self.get_proxy_list()
        return self.get_random_proxy()
    
    def is_expired(self, dt):
        """
        判断时间是否过期
        :param dt:日期字符串
        :return:True or False
        """
        if isinstance(dt, str):
            dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            return datetime.now() > dt
    def update_proxy(self):
        """
        重新通过api获取代理，更新代理
        """
        # 重新通过api获取代理
        self.proxy_list = self.get_proxy_list()
        new_proxy = self.get_random_proxy()
        return new_proxy
