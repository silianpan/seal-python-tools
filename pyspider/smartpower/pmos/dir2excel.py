#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/23 3:41 下午
# @Author  : silianpan
# @File    : dir2excel.py
# @Software: PyCharm
# 目录文件导出到Excel

import os

# 获取附件目录文件列表，如果没有在urlResultList里面，就删除
# def GetFileList(dir, fileList):
#     newDir = dir
#     if os.path.isfile(dir):
#         fileList.append(dir)
#     elif os.path.isdir(dir):
#         for s in os.listdir(dir):
#             # 如果需要忽略某些文件夹，使用以下代码
#             # if s == "xxx":
#             # continue
#             newDir = os.path.join(dir, s)
#             GetFileList(newDir, fileList)
#     return fileList
# fileList = GetFileList('/root/fileUpload/merchant/attachment', [])


def get_file_list(file_dir, file_list, source_dir, split_char='/'):
    """
    :param file_dir: 文件目录
    :param file_list: 文件结果列表
    :param source_dir: 源目录
    :param split_char: 分隔符
    :return: void
    """
    if os.path.isdir(file_dir):
        for s in os.listdir(file_dir):
            new_dir = os.path.join(file_dir, s)
            get_file_list(new_dir, file_list, source_dir)
    else:
        # 获取文件路径
        # 去掉source_dir
        # 替换/为.
        #print(file_dir)
        file_name = file_dir.replace(source_dir, '')
        file_name = file_name.lstrip('/')
        file_name = file_name.replace('/', split_char)
        file_name = file_name.replace('hsc.', '')
        if '.DS_Store' not in file_name:
            file_list.append(file_name)
