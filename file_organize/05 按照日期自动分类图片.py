#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm

from pathlib import Path
from datetime import datetime
from exifread import process_file
src_folder = Path('/Users/liupan/work/code/seal-python-tools/file_organize/要分类的图片/')
des_folder = Path('/Users/liupan/work/code/seal-python-tools/file_organize/分类后的图片/')
if not des_folder.exists():
    des_folder.mkdir(parents=True)
file_list = list(src_folder.glob('*.jpg'))
for i in file_list:
    with open(i, 'rb') as f:
        tags = process_file(f, details=False)
    if 'EXIF DateTimeOriginal' in tags.keys():
        dto = str(tags['EXIF DateTimeOriginal'])
        folder_name = datetime.strptime(dto, '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d')
        des_path = des_folder / folder_name
        if not des_path.exists():
            des_path.mkdir(parents=True)
        i.replace(des_path / i.name)
