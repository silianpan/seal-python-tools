#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm

import re
import shutil
import time
from urllib import parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

pdf_path = '/Users/liupan/work/code/seal-python-tools/pdf_process/公告/'

# Chrome选项
options = Options()
prefs = {'download.prompt_for_download': False,
         'download.default_directory': pdf_path}
options.add_experimental_option("prefs", prefs)
# 不打开浏览器
options.add_argument("--headless")

# 第一个参数chromedriver.exe绝对路径
browser = webdriver.Chrome(options=options)
url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=理财'
browser.get(url)
time.sleep(3)
data = browser.page_source
p_count = '<span class="total-box" style="">约(.*?)条'
# count = re.findall(p_count, data)[0]
count = 5
pages = int(int(count) / 10)
datas = []
datas.append(data)
for i in range(pages):
    browser.find_element_by_xpath('//*[@id="fulltext-search"]/div/div[1]/div[2]/div[4]/div[2]/div/button[2]').click()
    time.sleep(3)
    data = browser.page_source
    datas.append(data)
    time.sleep(3)

alldata = ''.join(datas)
browser.quit()
p_title = '<span title="" class="r-title">(.*?)</span>'
p_href = '<a target="_blank" href="(.*?)".*?<span title='
title = re.findall(p_title, alldata)
href = re.findall(p_href, alldata)
for i in range(len(title)):
    title[i] = re.sub('<.*?>', '', title[i])
    href[i] = 'http://www.cninfo.com.cn' + href[i]
    href[i] = re.sub('amp;', '', href[i])
    print(str(i + 1) + '.' + title[i])
    print(href[i])
for i in range(len(href)):
    browser = webdriver.Chrome(options=options)
    browser.get(href[i])
    time.sleep(3)

# 重命名
for i in range(len(href)):
    params = parse.parse_qs(parse.urlparse(href[i]).query)
    p_id = params['announcementId'][0]
    print(f'{pdf_path}{p_id}.PDF', f'{pdf_path}{str(i + 1)}.{title[i]}.PDF')
    shutil.move(f'{pdf_path}{p_id}.PDF', f'{pdf_path}{str(i + 1)}.{title[i]}.PDF')
