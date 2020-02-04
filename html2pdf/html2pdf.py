#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-02-04 11:04
# @Author  : liupan
# @Site    : 
# @File    : html2pdf.py
# @Software: PyCharm
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import uuid

import pdfkit
import pymysql

# file_path_root = '/mnt/data/pkulaw/'
file_path_root = '/Users/panliu/personal/seal-python-tools/html2pdf/pkulaw/'


def html2pdf(html_text, file_path):
    header = '<head><meta charset="UTF-8"></head>'
    pdfkit.from_string(header + html_text, file_path)
    return file_path


def start():
    # 读数据库
    db = pymysql.connect(host='localhost', user='root', password='Asdf@123', port=3306, db='pkulaw')
    cursor = db.cursor()
    cursor.execute('select title,url,content from law t where t.pdf_url is null')
    all_data = cursor.fetchall()
    for item in all_data:
        title = item[0]
        url = item[1]
        content = item[2]
        file_name = str(uuid.uuid4()) + '.pdf'
        file_path = file_path_root + file_name
        html2pdf(content, file_path)
        # 更新数据
        new_pdf_url = '/pkulaw/' + file_name
        sql = 'update law set pdf_url = %s where title = %s and url = %s and pdf_url is null'
        try:
            cursor.execute(sql, (new_pdf_url, title, url))
            db.commit()
        except:
            db.rollback()
        db.close()


if __name__ == '__main__':
    start()

