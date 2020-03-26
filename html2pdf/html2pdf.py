#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-02-04 11:04
# @Author  : liupan
# @Site    : 
# @File    : html2pdf.py
# @Software: PyCharm
import os
import sys
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf8')

import uuid

import pdfkit
import pymysql

# bus_list = [{'file_path':'/mnt/data/pkulaw/', 'db':'pkulaw'}, {'file_path':'/mnt/data/pkulaw_new/', 'db': 'pkulaw_new'}, {'file_path':'/mnt/data/pkulaw_other/', 'db': 'pkulaw_other'}]
bus_list = [{'file_path': '/mnt/data/pkulaw_other2/', 'db': 'pkulaw_other'}]


# bus_list = [{'file_path':'/mnt/data/pkulaw_new/', 'db': 'pkulaw_new'}]
# options = {
# 'quiet': ''
# }

def html2pdf(html_text, file_path):
    header = '<head><meta charset="UTF-8"></head>'
    try:
        pdfkit.from_string(header + html_text, file_path)
        return file_path
    except Exception as e:
        print('from_string error')


def bus_handle(file_path, mydb):
    # 读数据库
    db = pymysql.connect(host='localhost', user='root', password='Asdf@123', port=3306, db=mydb)
    cursor = db.cursor()
    # cursor.execute("select title,url,content from law t where t.pdf_url is null and t.content not like '%还不是用户？%'")
    cursor.execute("select title,url,content from law t where t.pdf_url is null")
    all_data = cursor.fetchall()
    for item in all_data:
        title = item[0]
        url = item[1]
        content = item[2]
        # 根据当前日期新建文件夹
        today_path = datetime.now().strftime('%Y%m%d')
        # 不存在就创建目录
        tmp_path = file_path + today_path
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
        file_name = str(uuid.uuid4()) + '.pdf'
        all_file_path = tmp_path + '/' + file_name
        html2pdf(content, all_file_path)
        # 更新数据
        new_pdf_url = 'upload/pkulaw_other2/' + today_path + '/' + file_name
        sql = 'update law set pdf_url = %s where title = %s and url = %s and pdf_url is null'
        try:
            cursor.execute(sql, (new_pdf_url, title, url))
            db.commit()
        except Exception as e:
            # db.rollback()
            print(e)
        # db.close()


def start():
    for item in bus_list:
        bus_handle(item['file_path'], item['db'])


if __name__ == '__main__':
    start()
