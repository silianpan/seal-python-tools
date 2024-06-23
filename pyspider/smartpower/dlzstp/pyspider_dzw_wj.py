#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-27
# @Author  : silianpan
# @Site    : 电力知识图谱-电知网-文件
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
            'Cookie': 'JSESSIONID=57e44891-bb43-41bb-9bde-2d7e4321e263; Hm_lvt_57ab5e4ca3c520d236a52dc5d78ed52e=1718983475,1719045270,1719103996; language=zh-CN; Hm_lpvt_57ab5e4ca3c520d236a52dc5d78ed52e=1719134984'
        }
    }

    def __init__(self):
        self.spider_config = {
            "source_url": 'https://www.dlzstp.com/dlzstp-guest/zstp/upload/pageGuest?page=1&limit=20&name=&suffix=&mode=&usageType=',
            'urls': [
                {'url': '', 'classify': 'qb', 'classify_name': u'全部', 'industry': u'文件'},
                {'url': 'standard', 'classify': 'bz', 'classify_name': u'标准', 'industry': u'文件'},
                {'url': 'report', 'classify': 'bg', 'classify_name': u'报告', 'industry': u'文件'},
                {'url': 'tutorial', 'classify': 'jc', 'classify_name': u'教程', 'industry': u'文件'},
                {'url': 'official', 'classify': 'zc', 'classify_name': u'政策', 'industry': u'文件'},
                {'url': 'thesis', 'classify': 'lw', 'classify_name': u'论文', 'industry': u'文件'},
                {'url': 'rule', 'classify': 'gf', 'classify_name': '规范', 'industry': u'文件'},
                {'url': 'original', 'classify': 'yc', 'classify_name': u'原创', 'industry': u'文件'},
                {'url': 'template', 'classify': 'mb', 'classify_name': u'模板', 'industry': u'文件'},
                {'url': 'other', 'classify': 'qt', 'classify_name': u'其他', 'industry': u'文件'},
            ],
            'db': {
                'host': '39.98.39.58',
                'user': 'root',
                'password': 'Asdf@123',
                'port': 3306,
                'dbname': 'smartpower-spider',
                'table_name': 'dlzstp_dzw_wj'
            },
            # 存储到本地的文件夹
            'file': {
                'out_dir': '/home/tmp/output/smartpower-spider/scdl/xxgk/',
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
        for i in range(1, 101):
           self.crawl(self.spider_config['source_url'] + item['url'] + '&page=' + str(i), save={'classify': item['classify'], 
                                                                            'classify_name': item['classify_name'],
                                                                            'industry': item['industry']},
                      validate_cert=False, method='GET', callback=self.next_page,
                      user_agent=UserAgent().random)

    @config(age=10 * 24 * 60 * 60)
    def next_page(self, response):
        if response.status_code == 200:
            ret = response.json
            if ret['code'] == 0:
                for item in ret['data']:
                    id = item['id']
                    self.crawl('https://www.dlzstp.com/dlzstp-guest/zstp/upload/downloadForWeb/' + id,
                       save={'classify': response.save['classify'], 'classify_name': response.save['classify_name'],
                             'industry': response.save['industry'], 'pub_date': item['createDate'],
                             'usage_type': item['usageType'], 'title': item['name'],
                             'page_cnt': item['pageCnt'], 'preview_cnt': item['previewCnt'],
                             'suffix': item['suffix'], 'download_cnt': item['downloadCnt'],
                             'mtype': item['mtype'], 'size': item['size'],
                             'year': item['year'], 'id': item['id'],},
                       validate_cert=False, method='GET', callback=self.detail_page,
                       user_agent=UserAgent().random)

    def item_page(self, response):
        pass

    @config(priority=2)
    def detail_page(self, response):
        if response.status_code == 200:
            ret = response.json
            if ret['code'] == 0:
                file_url = ret['data']
                file_id = response.save['id']
                file_type = response.save['suffix']
                file_name, file_path = self.download_file(file_url, file_id, file_type)
                content = ''
                with open(file_path, 'rb') as f:
                    content = base64.b64encode(f.read()).decode('utf-8')
                print('=======read.file========')
                print(content)
                obj = {
                   'medias': [{
                       'content': content,
                       'filename': '/page-medias/' + file_name
                   }]
                }
                ret = {
                    'id': md5string(url),
                    'url': file_url,
                    'classify': response.save['classify'],
                    'classify_name': response.save['classify_name'],
                    'title': response.save['title'],
                    'pub_date': response.save['pub_date'],
                    'json': json.dumps(obj, ensure_ascii=False),
                    'usage_type': response.save['usage_type'],
                    'page_cnt': response.save['page_cnt'],
                    'preview_cnt': response.save['preview_cnt'],
                    'suffix': response.save['suffix'],
                    'download_cnt': response.save['download_cnt'],
                    'mtype': response.save['mtype'],
                    'size': response.save['size'],
                    'year': response.save['year'],
                }
                self.save_to_mysql(self.spider_config['db']['table_name'], ret)
                return ret

    # 下载文件
    def download_file(self, file_url, file_id, file_type):
        file_name = file_id + '.' + file_type
        file_path = self.spider_config['file']['out_dir'] + file_name
        res = requests.get(file_url, verify=False)
        print('=======res.content========')
        print(res.content)
        with open(file_path, 'wb') as f:
            f.write(res.content)
        return file_name, file_path

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
