#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-27
# @Author  : silianpan
# @Site    : 苏州生物医药产业园-入驻企业
# @File    : spider_company.py
# @Software: PyCharm

import json
import os
import time
import requests

import pathlib
import pymysql
from fake_useragent import UserAgent
from pyspider.libs.base_handler import *
from urllib.parse import urlparse


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            'Connection': 'keep-alive',
            'Cookie': 'Hm_lvt_18ac8d8e0c79153d8b19f702982ed9f4=1612059392; Hm_lpvt_18ac8d8e0c79153d8b19f702982ed9f4=1612060127',
            'Host': 'www.biobay.com.cn',
            'Referer': 'http://www.biobay.com.cn/investor/customer/shangshiqiye/',
            'Upgrade-Insecure-Requests': '1',
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0'
        },
        'cookies': {
            'Hm_lpvt_18ac8d8e0c79153d8b19f702982ed9f4': '1612060127',
            'Hm_lvt_18ac8d8e0c79153d8b19f702982ed9f4': '1612059392'
        }
    }

    def __init__(self):
        self.custom_proxy = None
        self.spider_config = {
            "source_url": 'http://www.biobay.com.cn/investor/customer',
            'urls': [
                {'url': '/shangshiqiye/', 'classify': 'enterprise', 'classify_name': u'入驻客户'},
                {'url': '/xinyaochuangzhi/', 'classify': 'enterprise', 'classify_name': u'入驻客户'},
                {'url': '/yiliaoqixie/', 'classify': 'enterprise', 'classify_name': u'入驻客户'},
                {'url': '/shengwujishu/', 'classify': 'enterprise', 'classify_name': u'入驻客户'}
            ],
            'db': {
                'host': '172.19.249.124',
                'user': 'root',
                'password': 'Asdf@123',
                'port': 3306,
                'dbname': 'db-biotown-others',
                'table_name': 'spider_biobay'
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

    def get_proxy(self):
        ret = requests.get('http://http.tiqu.letecs.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4').json()
        return ret.get('data')[0].get('ip') + ':' + str(ret.get('data')[0].get('port'))

    @every(minutes=24 * 60)
    def on_start(self):
        self.custom_proxy = self.get_proxy()
        for item in self.spider_config['urls']:
            m_params = {
                'classify': item['classify'],
                'classify_name': item['classify_name'],
                'url': item['url']
            }
            self.crawl(self.spider_config['source_url'] + item['url'], fetch_type="js", save=m_params,
                       validate_cert=False, method='GET', callback=self.item_page,
                       user_agent=UserAgent().random, proxy=self.custom_proxy)

    @config(age=10 * 24 * 60 * 60)
    def item_page(self, response):
        boxs = response.doc('a[data-am-modal]').items()
        for box in boxs:
            am_modal = box.attr('data-am-modal').strip()
            am_modal = am_modal.replace('\'', '\"').replace('target', '\"target\"')\
                .replace('closeViaDimmer', '\"closeViaDimmer\"')\
                .replace('width', '\"width\"').replace('height', '\"height\"')
            target = json.loads(am_modal)
            target = target['target']
            content = response.doc(target).html().strip()
            title = box.text().strip()
            save = {
                'title': title,
                'content': content
            }
            self.detail_page2(response, save)
            # self.crawl('http://httpbin.org/get', fetch_type="js", save=save,
            #            validate_cert=False, method='GET', callback=self.detail_page,
            #            user_agent=UserAgent().random)

    @config(priority=2)
    def detail_page(self, response):
        ret = {
            'id': md5string(response.url),
            'url': response.url,
            'title': response.save['title'],
            'content': response.save['content'].replace(u'\xa0', '').replace(u'\t', '').replace(u'\n', '').replace(u'\u2002', '').replace(u'\u3000', ''),
            'classify_name': response.save['classify_name'],
            'classify': response.save['classify']
        }
        local_json_file = self.build_local_json_file(response)
        ret['json_url'] = local_json_file['json_url']
        self.save_to_json(local_json_file['file_path'], ret)
        self.save_to_mysql(self.spider_config['db']['table_name'], ret)
        return ret

    @config(priority=2)
    def detail_page2(self, response, save):
        ret = {
            'id': md5string(response.url),
            'url': response.url,
            'title': save['title'],
            'content': save['content'].replace(u'\xa0', '').replace(u'\t', '').replace(u'\n', '').replace(u'\u2002', '').replace(u'\u3000', ''),
            'classify_name': response.save['classify_name'],
            'classify': response.save['classify']
        }
        local_json_file = self.build_local_json_file(response)
        ret['json_url'] = local_json_file['json_url']
        self.save_to_json(local_json_file['file_path'], ret)
        self.save_to_mysql(self.spider_config['db']['table_name'], ret)
        return ret

    # 构建本地存储json文件
    def build_local_json_file(self, response):
        pr = urlparse(response.url)
        partitions = pr.path.partition('.')
        out_dir = self.spider_config['file']['out_dir']
        # db.yaozh.com => dbyaozhcom
        source = pr.netloc.replace('.', '')
        # 日期：2020-11-12
        now_day = time.strftime('%Y-%m-%d', time.localtime())
        # /Users/hsc/CodeWorkSpace/projects/tianfu-bio-town/code/biotown-parent/spider/dbyaozhcom
        p_dir = os.path.join(out_dir, "{0}/{1}".format(source, now_day))
        # /policies/6247.json
        file_name = partitions[0] + pr.query.replace('=', '_').replace('&', '_') + '.json'
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
