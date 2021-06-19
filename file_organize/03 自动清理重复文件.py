#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm

from pathlib import Path
from filecmp import cmp
src_folder = Path('/Users/liupan/work/code/seal-python-tools/file_organize/图片/')
des_folder = Path('/Users/liupan/work/code/seal-python-tools/file_organize/图片/重复的图片/')
if not des_folder.exists():
    des_folder.mkdir(parents=True)
result = list(src_folder.glob('*'))
file_list = []
for i in result:
    if i.is_file():
        file_list.append(i)
for m in file_list:
    for n in file_list:
        if m != n and m.exists() and n.exists():
            if cmp(m, n):
                n.replace(des_folder / n.name)

