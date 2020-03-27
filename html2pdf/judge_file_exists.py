#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/27 上午9:09
# @Author  : liupan
# @Site    : 
# @File    : judgeFileExists.py
# @Software: PyCharm

import os
import pymysql

# 获取附件目录文件列表，如果没有在urlResultList里面，就删除
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            # if s == "xxx":
            # continue
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList

fileList = GetFileList('/mnt/data/pkulaw_other', [])
allDirList = []
for fileItem in fileList:
    # 如果存在改文件
    if os.path.exists(fileItem):
        fileName = os.path.basename(fileItem)
        allDirList.append(fileName)


db = pymysql.connect(host='localhost', user='root', password='Asdf@123', port=3306, db='pkulaw_other')
cursor = db.cursor()
cursor.execute("select title,url,pdf_url from law t where t.pdf_url is not null and t.pdf_url like '/pkulaw/%'")
all_data = cursor.fetchall()

urlResultList = []
for item in all_data:
    title = item[0]
    url = item[1]
    pdf_url = item[2]
    new_id = pdf_url[-40:]
    if new_id not in allDirList:
        urlResultList.append(new_id + '\n')

f = open('file_not_exists.txt', 'w')
f.writelines(urlResultList)
f.close()
