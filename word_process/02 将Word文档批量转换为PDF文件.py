#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : file.py
# @Software: PyCharm

from pathlib import Path
from comtypes.client import CreateObject
src_folder = Path('/Users/liupan/work/code/seal-python-tools/word_process/合同文件/')
des_folder = Path('/Users/liupan/work/code/seal-python-tools/word_process/PDF文件/')
if not des_folder.exists():
    des_folder.mkdir(parents=True)
file_list = list(src_folder.glob('*.docx'))
word = CreateObject('Word.Application')
for word_path in file_list:
    pdf_path = des_folder / word_path.with_suffix('.pdf').name
    if pdf_path.exists():
        continue
    else:
        doc = word.Documents.Open(str(word_path))
        doc.SaveAs(str(pdf_path), FileFormat=17)
        doc.Close()
word.Quit()