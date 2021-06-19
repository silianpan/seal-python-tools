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
for pdf in file_list:
    inputfile = PdfFileReader(str(pdf))
    outputfile = PdfFileWriter()
    pageCount = inputfile.getNumPages()
    for page in range(pageCount):
        outputfile.addPage(inputfile.getPage(page))
    outputfile.encrypt('123456')
    des_name = f'{pdf.stem}_secret.pdf'
    des_file = src_folder / des_name
    with open(des_file, 'wb') as f_out:
        outputfile.write(f_out)
