#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm

import os
import shutil
src_folder = '/Users/liupan/work/code/seal-python-tools/file_organize/要分类的文件/'
des_folder = '/Users/liupan/work/code/seal-python-tools/file_organize/分类后的文件/'
files = os.listdir(src_folder)
print(files)
for i in files:
    src_path = src_folder + i
    if os.path.isfile(src_path):
        des_path = des_folder + i.split('.')[-1]
        if not os.path.exists(des_path):
            os.makedirs(des_path)
        shutil.move(src_path, des_path)