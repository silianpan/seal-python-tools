#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : file.py
# @Software: PyCharm

from pathlib import Path
from zipfile import ZipFile
import win32com.client as win32
def ppt2pptx(ppt_path):
    ppt_app = win32.gencache.EnsureDispatch('PowerPoint.Application')
    ppt = ppt_app.Presentations.Open(ppt_path)
    pptx_path = ppt_path.with_suffix('.pptx')
    ppt.SaveAs(pptx_path, 24)
    ppt.Close()
    ppt_app.Quit()
    return pptx_path
def extract_img(ppt_path, img_folder):
    if ppt_path.suffix == '.ppt':
        ppt_path = ppt2pptx(ppt_path)
    with ZipFile(ppt_path) as zf:
        for name in zf.namelist():
            if name.startswith('ppt/media/image'):
                zf.extract(name, img_folder)
pptx_file = Path('/Users/liupan/work/code/seal-python-tools/ppt_process/PPT模板.pptx')
img_folder = Path('/Users/liupan/work/code/seal-python-tools/ppt_process/图片素材/')
if not img_folder.exists():
    img_folder.mkdir(parents=True)
extract_img(pptx_file, img_folder)
