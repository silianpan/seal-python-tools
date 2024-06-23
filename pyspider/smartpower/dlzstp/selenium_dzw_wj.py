#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-06-16
# @Author  : silianpan
# @Site    : 旗帜领航-专题专栏
# @File    : spider_news.py
# @Software: PyCharm

import base64
from time import sleep
import pymysql
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote

class Handler():
    def __init__(self):
        self.spider_config = {
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
                # 'out_dir': '/home/tmp/output/smartpower-spider/dlzstp/wj/',
                'out_dir': '/Users/liupan/Downloads/',
            }
        }
        self.conn = pymysql.connect(host=self.spider_config['db']['host'], user=self.spider_config['db']['user'],
                                    password=self.spider_config['db']['password'],
                                    port=self.spider_config['db']['port'],
                                    db=self.spider_config['db']['dbname'])
        self.cursor = self.conn.cursor()

        # chrome driver init
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.binary_location = '/Users/liupan/Downloads/chrome-mac-x64/'
        service = webdriver.chrome.service.Service('/Users/liupan/Downloads/chromedriver-mac-x64/chromedriver')
        self.browser = webdriver.Chrome(service=service, options=chrome_options)
        self.browser.maximize_window()

        self.wait = WebDriverWait(self.browser, 1000)

        def interceptor(request):
            request.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        self.browser.request_interceptor = interceptor

    def index_page(self):
        # 查询获取数据库的所有结果
        all_titles = self.select_titles()

        self.browser.get('https://www.dlzstp.com/')

        login_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        login_btn.click()

        self.browser.implicitly_wait(10000)
        sleep(10)
        # browser.get('https://www.dlzstp.com/dlzstp-guest/zstp/upload/pageGuest?page=1&limit=20&name=&suffix=&mode=&usageType=')
        self.browser.get('https://www.dlzstp.com/file/list')
        sleep(2)
        for i in range(0, 101):
            items = self.browser.find_elements(By.CSS_SELECTOR, '.wraterfall-item > .item')
            for item in items:
                title = item.find_element(By.CSS_SELECTOR, '.wraterfall-item > .item > .right > .title')
                title = title.text.strip()
                print(title)
                if title in all_titles:
                    continue
                pub_date = item.find_element(By.CSS_SELECTOR, '.wraterfall-item > .item > .right > .info > .flex > div:first-child')
                pub_date = pub_date.text.strip()

                # 打开对话框
                self.browser.execute_script("arguments[0].click()", item)
                # 下载
                download_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.toolbar > button.el-button')))
                self.browser.execute_script("arguments[0].click()", download_btn)
                sleep(2)
                # 关闭窗口
                # close_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.el-dialog__header > button.el-dialog__headerbtn')))
                close_btn = self.browser.find_element(By.CSS_SELECTOR, '.el-dialog__header > button.el-dialog__headerbtn')
                self.browser.execute_script("arguments[0].click()", close_btn)
                self.save_file_data(self, {
                    'title': title,
                    'pub_date': pub_date,
                })
                sleep(3)
            # 向下滑动1000像素
            # browser.execute_script('window.scrollBy(0,1000)')
            # 执行 JavaScript 代码滚动到页面底部
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(5)

    # 查询所有标题
    def select_titles(self):
        sql = "select distinct title from dlzstp_dzw_wj"
        try:
            self.cursor.execute(sql)
            print('Count:', self.cursor.rowcount)
            rows = self.cursor.fetchall()
            print(rows)
            return rows
        except:
            print('Error')
            return []

    def save_file_data(self, data):
        title = data['title']
        file_path = self.spider_config['file']['out_dir'] + title
        content = ''
        with open(file_path, 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        print('=======read.file========')
        print(content)
        obj = {
           'medias': [{
               'content': content,
               'filename': '/page-medias/' + title
           }]
        }
        ret = {
            'id': md5string(title),
            'title': title,
            'pub_date': data['pub_date'],
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

    def main(self):
        self.index_page()

if __name__ == '__main__':
    Handler().main()
