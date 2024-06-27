#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-27
# @Author  : silianpan
# @Site    : 国家电网-旗帜领航-专题专栏
# @File    : spider_news.py
# @Software: PyCharm

import base64
import json
import hashlib
from mysql_util import MysqlUtil

from dir2excel import get_file_list

if __name__ == '__main__':
  mu = MysqlUtil('8.137.8.225', 'smartpower-spider', 'root', 'Spider@123', 33306)
  md5_hash = hashlib.md5()
  dir = '/Users/liupan/Downloads/smartpower-spider/四川电力交易中心'
  file_list = []
  get_file_list(dir, file_list, dir, split_char='/')
  #print(file_list)
  for file in file_list:
    content = ''
    with open(dir + '/' + file, 'rb') as f:
        content = base64.b64encode(f.read()).decode('utf-8')
    #print('=======read.file========')
    #print(content)
    file_split = file.split('/')
    first = file_split[0]
    second = file_split[1]
    file_name = file_split[2]
    #print(first, second, file_name)
    obj = {
       'medias': [{
           'content': content,
           'filename': '/page-medias/' + file_name
       }]
    }
    md5_hash.update(file.encode('utf-8'))
    id = md5_hash.hexdigest()
    #print(id)
    ret = {
      'id': id,
      'title': file_name,
      'url': file,
      'first': first,
      'second': second,
      'content': content,
      'json': json.dumps(obj, ensure_ascii=False),
    }
    #print(ret)
    mu.insert('scdl_jyzx', **ret)