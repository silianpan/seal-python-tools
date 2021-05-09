#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : file.py
# @Software: PyCharm

from pathlib import Path
import xlwings as xw
import pandas as pd
src_folder = Path('/Users/liupan/work/code/seal-python-tools/excel_process/每月进货统计表/')
file_list = list(src_folder.glob('*.xlsx'))
app = xw.App(visible=False, add_book=False)
for i in file_list:
    if i.name.startswith('~$'):
        continue
    workbook = app.books.open(i)
    worksheet = workbook.sheets['Sheet1']
    data = worksheet.range('A1').options(pd.DataFrame, header=1, index=False, expand='table').value
    new_data = data['产品尺寸（mm）'].str.split('*', expand=True)
    new_data.columns = ['长（mm）', '宽（mm）', '高（mm）']
    for j in range(new_data.shape[1] - 1):
        worksheet['F:F'].insert(shift='right', copy_origin='format_from_left_or_above')
    worksheet['F1'].options(index=False).value = new_data
    worksheet.autofit()
    workbook.save()
    workbook.close()
app.quit()
