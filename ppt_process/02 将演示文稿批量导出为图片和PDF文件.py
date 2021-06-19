#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : file.py
# @Software: PyCharm

import win32com.client as win32
from pathlib import Path
def ppt_conv(ppt_path):
    ppt_app = win32.gencache.EnsureDispatch('PowerPoint.Application')
    ppt = ppt_app.Presentations.Open(ppt_path)
    jpg_path = ppt_path.with_suffix('.jpg')
    pdf_path = ppt_path.with_suffix('.pdf')
    ppt.SaveAs(jpg_path, 17)
    ppt.SaveAs(pdf_path, 32)
    ppt.Close()
    ppt_app.Quit()
file_path = Path('/Users/liupan/work/code/seal-python-tools/ppt_process/PPT文件/')
file_list = file_path.glob('*.ppt*')
for i in file_list:
    if i.is_file():
        ppt_conv(i)
