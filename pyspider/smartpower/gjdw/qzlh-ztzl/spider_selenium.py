#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-06-16
# @Author  : silianpan
# @Site    : 旗帜领航-专题专栏
# @File    : spider_news.py
# @Software: PyCharm

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote

# browser = webdriver.Chrome()
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

wait = WebDriverWait(browser, 10)

def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        url = 'http://www.sgcc.com.cn/html/sgcc/col2022121491/column_2022121491_' + page + '.shtml'
        browser.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_list()
    except TimeoutException:
        index_page(page)

def get_list():
    """
    提取列表数据
    """
    html = browser.page_source
    doc = pq(html)
    items = doc('.newslist > li').items()
    for item in items:
      href = item.find('a').attr('href')
      title = item.find('a').attr('title')
      pub_date = item.find('i').text().strip()
      print(href, title, pub_date)

def main():
    page = 1
    index_page(page)

if __name__ == '__main__':
    main()
