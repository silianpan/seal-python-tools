#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-27
# @Author  : silianpan
# @Site    : 山东国际生物科技园-新闻动态
# @File    : spider_news.py
# @Software: PyCharm

import json
import os
import time

import pathlib
import pymysql
from pyspider.libs.base_handler import *
from urllib.parse import urlparse


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
        }
    }

    def __init__(self):
        self.spider_config = {
            "source_url": 'http://www.bioasis.cn/news',
            'urls': [
                {'url': '/yuanquxinwen.jsp', 'classify': 'news', 'classify_name': u'园区新闻'},
                {'url': '/xingyexinwen.jsp', 'classify': 'news', 'classify_name': u'行业新闻'},
            ],
            'db': {
                'host': '192.168.0.103',
                'user': 'root',
                'password': 'Asdf@123',
                'port': 3306,
                'dbname': 'db-biotown-others',
                'table_name': 'spider_bioasis'
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
            m_params = {
                'classify': item['classify'],
                'classify_name': item['classify_name'],
                'url': item['url'],
                'nowPage': 1
            }
            self.crawl(self.spider_config['source_url'] + item['url'], params=m_params, save=m_params,
                       fetch_type="js", validate_cert=False, method='GET', callback=self.next_page)

    @config(age=10 * 24 * 60 * 60)
    def next_page(self, response):
        # 爬取详细文章
        self.item_page(response)
        # 继续爬取下一页列表
        pnext = response.doc('.paging-next').text()
        pmid_num = response.doc('.paging > .pageing-middle:last').text().strip()
        pcur_num = response.doc('.paging > .cur').text().strip()
        if (u'下一页' in pnext) and (int(pmid_num) + 1 != int(pcur_num)):
            new_params = response.save
            new_params['nowPage'] = int(new_params['nowPage']) + 1
            self.crawl(self.spider_config['source_url'] + new_params['url'],
                       params=new_params,
                       save=new_params, fetch_type="js",
                       validate_cert=False, method='GET', callback=self.next_page)

    def item_page(self, response):
        boxs = response.doc('.newsList > .nl').items()
        for box in boxs:
            pub_date = box('.nlt').text().strip()
            art_href = box('.nli > h3 > a').attr('href')
            self.crawl(art_href, validate_cert=False,
                       save={'pub_date': pub_date, 'classify_name': response.save['classify_name'],
                             'classify': response.save['classify']}, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.listcontent > .newsDetailTitle').text().strip()
        content = response.doc('.listcontent > .textarea').html().strip()
        ret = {
            'id': md5string(response.url),
            'url': response.url,
            'title': title,
            'content': content.replace(u'\xa0', '').replace(u'\t', '').replace(u'\n', '').replace(u'\u2002', '').replace(u'\u3000', ''),
            'pub_date': response.save['pub_date'],
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
