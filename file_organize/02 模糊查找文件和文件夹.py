#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm

from pathlib import Path
while True:
    folder = input('请输入要在哪个文件夹（如【D:\\】或【D:\\案例\\】）下进行查找：')
    folder = Path(folder.strip())
    if folder.exists() and folder.is_dir():
        break
    else:
        print('输入的路径不存在或不正确，请重新输入！')
keyword = input('请输入要查找的文件或文件夹的名称：').strip()
result = list(folder.rglob(f'*{keyword}*'))
if len(result) == 0:
    print(f'在【{folder}】下未查找到名称包含关键词【{keyword}】的文件或文件夹！')
else:
    result_folder = []
    result_file = []
    for i in result:
        if i.is_dir():
            result_folder.append(i)
        else:
            result_file.append(i)
    if len(result_folder) != 0:
        print(f'在【{folder}】下查找到以下名称包含关键词【{keyword}】的文件夹：')
        for i in result_folder:
            print(i)
    if len(result_file) != 0:
        print(f'在【{folder}】下查找到以下名称包含关键词【{keyword}】的文件：')
        for i in result_file:
            print(i)
