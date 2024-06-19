#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-27
# @Author  : silianpan
# @Site    : 四川电力-信息公开
# @File    : scdl_xxgk.py
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
        # 'timeout': 2,
        'headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.sc.sgcc.com.cn',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        }
    }

    def __init__(self):
        self.proxy_list = self.get_proxy_list()
        self.spider_config = {
            "source_url": 'https://www.sc.sgcc.com.cn/html/main',
            'urls': [
                {'url': '/col2795/column_2795_1.html', 'classify': 'gwscsdlgsjj', 'classify_name': u'国网四川省电力公司简介'},
                {'url': '/col2794/column_2794_1.html', 'classify': 'blydywcxjsx', 'classify_name': u'办理用电业务程序及时限'},
                {'url': '/col2796/column_2796_1.html', 'classify': 'gdqydjhsfbz', 'classify_name': u'供电企业电价和收费标准'},
                {'url': '/col2799/column_2799_1.html', 'classify': 'gdzlhllqk', 'classify_name': u'供电质量和两率情况'},
                {'url': '/col2798/column_2798_1.html', 'classify': 'gdfwxgflfg', 'classify_name': u'供电服务相关法律法规'},
                {'url': '/col2800/column_2800_1.html', 'classify': 'fwcnjtsdh', 'classify_name': u'服务承诺及投诉电话'},
                {'url': '/col2801/column_2801_1.html', 'classify': 'yhsdgcxgxx', 'classify_name': u'用户受电工程相关信息'},
                {'url': '/col2803/column_2803_1.html', 'classify': 'scsnrgjjczbtgmhygfxmgs', 'classify_name': u'四川省纳入国家财政补贴规模户用光伏项目公示'},
                {'url': '/col2804/column_2804_1.html', 'classify': 'dlgdygsxgg', 'classify_name': u'代理购电有关事项公告'},
                {'url': '/col2791/column_2791_1.html', 'classify': 'ysqxxgknr', 'classify_name': u'依申请信息公开内容'},
                {'url': '/col2792/column_2792_1.html', 'classify': 'xxgkzn', 'classify_name': u'信息公开指南'},
            ],
            'db': {
                'host': '39.98.39.58',
                'user': 'root',
                'password': 'Asdf@123',
                'port': 3306,
                'dbname': 'smartpower-spider',
                'table_name': 'scdl_xxgk'
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
           self.crawl(self.spider_config['source_url'] + item['url'], save={'classify': item['classify'], 'classify_name': item['classify_name']},
                      validate_cert=False, method='GET', callback=self.next_page, proxy='http://{proxy}'.format(proxy=self.get_random_proxy()),
                      user_agent=UserAgent().random)

    @config(age=10 * 24 * 60 * 60)
    def next_page(self, response):
        # 爬取详细文章
        self.item_page(response)
        pageCount = response.doc('.pagenav > form > #pagenavpagecount > b').text().strip()
        for i in range(2, int(pageCount) + 1):
            self.crawl(response.url.replace('1.html', str(i) + '.html'),
                       save={'classify': response.save['classify'], 'classify_name': response.save['classify_name']},
                       validate_cert=False, method='GET', callback=self.item_page, proxy='http://{proxy}'.format(proxy=self.get_random_proxy()),
                       user_agent=UserAgent().random)

    def item_page(self, response):
        if response.status_code in [401, 403, 599]:
            self.crawl(response.url, save={'classify': response.save['classify'], 'classify_name': response.save['classify_name']},
                       validate_cer=False, method='GET', callback=self.item_page, proxy='http://{proxy}'.format(proxy=self.update_proxy()),
                       user_agent=UserAgent().random)

        boxs = response.doc('ul.list > li').items()
        for box in boxs:
            art_href = box('a').attr('href')
            if 'portal.sc.sgcc.com.cn' not in art_href:
                ## 判断是否是文档链接
                file_ext = art_href[art_href.rfind('.') + 1:]
                if file_ext in ['pdf', 'doc', 'xls', 'ppt', 'docx', 'xlsx', 'pptx', 'png', 'jpg']:
                   self.download_file(art_href)
                   file_name = art_href[art_href.rfind('/') + 1:]
                   file_path = self.spider_config['file']['out_dir'] + file_name
                   self.save_file_data(file_name, file_path, art_href, response.save)
                else:
                    art_title = box('a').text().strip()
                    pub_date = box('span').text().strip()
                    self.crawl(art_href, validate_cert=False,
                               save={'pub_date': pub_date, 'title': art_title, 'classify': response.save['classify'],
                                     'classify_name': response.save['classify_name']}, callback=self.detail_page, proxy='http://{proxy}'.format(proxy=self.get_random_proxy()),
                                     user_agent=UserAgent().random)

    @config(priority=2)
    def detail_page(self, response):
        if response.status_code in [401, 403, 599]:
            self.crawl(response.url, save={'classify': response.save['classify'], 'classify_name': response.save['classify_name']},
                       validate_cer=False, method='GET', callback=self.item_page, proxy='http://{proxy}'.format(proxy=self.update_proxy()),
                       user_agent=UserAgent().random)
        content = response.doc('.txtcon').html().strip()
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
            'json': json.dumps(obj, ensure_ascii=False)
        }
        self.save_to_mysql(self.spider_config['db']['table_name'], ret)
        return ret

    # 保存文件数据
    def save_file_data(self, file_name, file_path, url, save):
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
            'url': url,
            'classify': save['classify'],
            'classify_name': save['classify_name'],
            'title': save['title'],
            'pub_date': save['pub_date'],
            'json': json.dumps(obj, ensure_ascii=False)
        }
        self.save_to_mysql(self.spider_config['db']['table_name'], ret)
        return ret

    # 下载文件
    def download_file(self, file_url):
        file_name = file_url[file_url.rfind('/') + 1:]
        file_path = self.spider_config['file']['out_dir'] + file_name
        new_proxy = 'http://{proxy}'.format(proxy=self.get_random_proxy())
        proxies = {'http': new_proxy, 'https': new_proxy}
        res = requests.get(file_url, verify=False, proxies=proxies)
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