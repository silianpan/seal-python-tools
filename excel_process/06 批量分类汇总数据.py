#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : file.py
# @Software: PyCharm

import xlwings as xw
import pandas as pd
app = xw.App(visible=False, add_book=False)
workbook = app.books.open('/Users/liupan/work/code/seal-python-tools/excel_process/产品销售统计表.xlsx')
worksheets = workbook.sheets
table = pd.DataFrame()
for i, j in enumerate(worksheets):
    data = j.range('A1').options(pd.DataFrame, header=1, index=False, expand='table').value
    data = data.reindex(columns=['单号', '销售日期', '产品名称', '成本价（元/个）', '销售价（元/个）', '销售数量（个）', '产品成本（元）', '销售收入（元）', '销售利润（元）'])
    table = table.append(data, ignore_index=True)
table = table.groupby('产品名称')
new_workbook = xw.books.add()
for idx, group in table:
    new_worksheet = new_workbook.sheets.add(idx)
    new_worksheet['A1'].options(index=False).value = group
    last_cell = new_worksheet['A1'].expand('table').last_cell
    last_row = last_cell.row
    last_column = last_cell.column
    last_column_letter = chr(64 + last_column)
    sum_cell_name = f'{last_column_letter}{last_row + 1}'
    sum_last_row_name = f'{last_column_letter}{last_row}'
    formula = f'=SUM({last_column_letter}2:{sum_last_row_name})'
    new_worksheet[sum_cell_name].formula = formula
    new_worksheet.autofit()
new_workbook.save('F:\\代码文件\\第6章\\产品销售统计表（已汇总）.xlsx')
app.quit()
