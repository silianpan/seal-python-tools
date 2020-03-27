#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/26 下午11:52
# @Author  : liupan
# @Site    : 
# @File    : add_id.py
# @Software: PyCharm

# pdf_url[-40:-4]

import pymysql

bus_list = [{'db': 'pkulaw_other'}]


def bus_handle(mydb):
    # 读数据库
    db = pymysql.connect(host='localhost', user='root', password='Asdf@123', port=3306, db=mydb)
    cursor = db.cursor()
    cursor.execute("select title,url,pdf_url from law t where t.pdf_url is not null and t.id is null")
    all_data = cursor.fetchall()
    for item in all_data:
        title = item[0]
        url = item[1]
        pdf_url = item[2]

        new_id = pdf_url[-40:-4]
        sql = 'update law set id = %s where title = %s and url = %s'
        try:
            cursor.execute(sql, (new_id, title, url))
            db.commit()
        except Exception as e:
            # db.rollback()
            print(e)
        # db.close()


def start():
    for item in bus_list:
        bus_handle(item['db'])


if __name__ == '__main__':
    start()
