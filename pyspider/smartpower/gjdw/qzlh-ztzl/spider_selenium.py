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
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)

wait = WebDriverWait(browser, 1000)

def interceptor(request):
    request.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    request.headers['Accept-Encoding'] = 'gzip, deflate'
    request.headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6'
    request.headers['Cache-Control'] = 'max-age=0'
    request.headers['Host'] = 'www.sgcc.com.cn'
    request.headers['Upgrade-Insecure-Requests'] = '1'
    request.headers['Proxy-Connection'] = 'keep-alive'
    request.headers['Cookie'] = 'Rq9ZlcGkVvC3S=60krow3RM27oI7EaMaEmYqgtES_ByaGvNdoSaqdM9lZu6HFHaZjMQObOi2QdoU0P7Omq_vUwFFYWg9CdBV4VLqoq; Rq9ZlcGkVvC3T=0Bxm2wXgUkFnHY754YCzFFuTDtPq_v44jRvx6y8llhJzD1zAqiyjHQXadBZw._zH9ciRjYg95jph3CjJETjLPuP1csu099mmRT1tujRMFiyjA4PsUXCLf667sFM.9c6oNHu_uVFmLjhkmxS2DFmTNCC90rYp5swNMJuL8u9kH4spGskr2YwXN7htuJNFFYQSXuRnFSYDOlr9NFcYyOifkCtcov36OPruSR4li_iWn3SjnJaJc7SSp0iX6kcya5nOAaDgLXQRrCY9BLwkqB9Ea6UQCAlYMVBLiTLzqrzznw4D74.n1hzcwmXfSVl8KxVntR9tystVxhBM7WvJZVbTxwrXNfFlmoJm3.Ni.xbW61Mg'

browser.request_interceptor = interceptor

def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    # try:
    url = 'http://www.sgcc.com.cn/html/sgcc/col2022121491/column_2022121491_' + str(page) + '.shtml'
    print(url)
    browser.get(url)
    # 执行JavaScript代码
    browser.execute_script('document.documentElement.scrollTop = document.documentElement.scrollHeight')
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'newslist')))
    get_list()
    # except TimeoutException:
    #     index_page(page)

def get_list():
    """
    提取列表数据
    """
    html = browser.page_source
    print(html)
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
