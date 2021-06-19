#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm

from pathlib import Path
src_folder = Path('/Users/liupan/work/code/seal-python-tools/file_organize/要分类的文件/')
des_folder = Path('/Users/liupan/work/code/seal-python-tools/file_organize/分类后的文件/')
files = src_folder.glob('*')
for i in files:
    if i.is_file():
        des_path = des_folder / i.suffix.strip('.')
        if not des_path.exists():
            des_path.mkdir(parents=True)
        i.replace(des_path / i.name)