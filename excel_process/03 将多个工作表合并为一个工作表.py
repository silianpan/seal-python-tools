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
sheet_name = '产品销售统计'
header = None
all_data = []
for i in file_list:
    if i.name.startswith('~$'):
        continue
    workbook = app.books.open(i)
    for j in workbook.sheets:
        if j.name == sheet_name:
            if header is None:
                header = j['A1:I1'].value
            data = j['A2'].expand('table').value
            all_data = all_data + data
    workbook.close()
new_workbook = xw.Book()
new_worksheet = new_workbook.sheets.add(sheet_name)
new_worksheet['A1'].value = header
new_worksheet['A2'].value = all_data
new_worksheet.autofit()
new_workbook.save(src_folder / '上半年产品销售统计表.xlsx')
new_workbook.close()
app.quit()
