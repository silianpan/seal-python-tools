#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm

from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter

src_folder = Path('/Users/liupan/work/code/seal-python-tools/pdf_process/公告/')
file_list = list(src_folder.glob('*.PDF'))
step = 5
for pdf in file_list:
    inputfile = PdfFileReader(str(pdf))
    pages = inputfile.getNumPages()
    if pages <= step:
        print(f'【{pdf.name}】页数为{pages}，小于等于每份页数{step}，不做拆分')
        continue
    parts = pages // step + 1
    for pt in range(parts):
        start = step * pt
        if pt != (parts - 1):
            end = start + step - 1
        else:
            end = pages - 1
        outputfile = PdfFileWriter()
        for pn in range(start, end + 1):
            outputfile.addPage(inputfile.getPage(pn))
        pt_name = f'{pdf.stem}_第{pt + 1}部分.pdf'
        pt_file = src_folder / pt_name
        with open(pt_file, 'wb') as f_out:
            outputfile.write(f_out)
    print(f'【{pdf.name}】页数为{pages}，拆分为{parts}部分')
