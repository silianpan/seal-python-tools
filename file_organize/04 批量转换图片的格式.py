#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm

from pathlib import Path
from PIL import Image
src_folder = Path('/Users/liupan/work/code/seal-python-tools/file_organize/要转换格式的图片/')
des_folder = Path('/Users/liupan/work/code/seal-python-tools/file_organize/转换格式后的图片/')
if not des_folder.exists():
    des_folder.mkdir(parents=True)
file_list = list(src_folder.glob('*.jpg'))
for i in file_list:
    des_file = des_folder / i.name
    des_file = des_file.with_suffix('.png')
    Image.open(i).save(des_file)
    print(f'{i.name} 完成格式转换！')
