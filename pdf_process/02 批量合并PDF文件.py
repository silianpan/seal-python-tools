#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm

from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileMerger

src_folder = Path('/Users/liupan/work/code/seal-python-tools/pdf_process/公告/')
des_file = Path('/Users/liupan/work/code/seal-python-tools/pdf_process/公告/合并后的公告文件.PDF')
if not des_file.parent.exists():
    des_file.parent.mkdir(parents=True)
file_list = list(src_folder.glob('*.PDF'))
merger = PdfFileMerger()
outputPages = 0
for pdf in file_list:
    inputfile = PdfFileReader(str(pdf))
    merger.append(inputfile)
    pageCount = inputfile.getNumPages()
    print(f'{pdf.name}  页数：{pageCount}')
    outputPages += pageCount
merger.write(str(des_file))
merger.close()
print(f'\n合并后的总页数：{outputPages}')
