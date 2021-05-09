#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : file.py
# @Software: PyCharm

from pathlib import Path
import xlwings as xw
src_folder = Path('/Users/liupan/work/code/seal-python-tools/excel_process/月销售统计/')
file_list = list(src_folder.glob('*.xlsx'))
app = xw.App(visible=False, add_book=False)
for i in file_list:
    if i.name.startswith('~$'):
        continue
    workbook = app.books.open(i)
    for j in workbook.sheets:
        data = j['A2'].expand('table').value
        for index, val in enumerate(data):
            if val[2] == '背包':
                val[2] = '双肩包'
                data[index] = val
        j['A2'].expand('table').value = data
    workbook.save()
    workbook.close()
app.quit()
