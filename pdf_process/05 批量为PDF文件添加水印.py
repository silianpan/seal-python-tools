#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm

from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import reportlab.pdfbase.ttfonts

def create_watermark(content):
    file_name = '水印.pdf'
    a = canvas.Canvas(file_name, pagesize=(30 * cm, 30 * cm))
    a.translate(5 * cm, 0 * cm)
    reportlab.pdfbase.pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont('阿里巴巴普惠体', '/Users/liupan/work/code/seal-python-tools/pdf_process/Alibaba-PuHuiTi-Regular.ttf'))
    a.setFont('阿里巴巴普惠体', 25)
    a.rotate(30)
    a.setFillColorRGB(0, 0, 0)
    a.setFillAlpha(0.2)
    for i in range(0, 30, 5):
        for j in range(0, 30, 5):
            a.drawString(i * cm, j * cm, content)
    a.save()
    return file_name
def add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    outputfile = PdfFileWriter()
    inputfile = PdfFileReader(pdf_file_in)
    pageCount = inputfile.getNumPages()
    markfile = PdfFileReader(pdf_file_mark)
    for i in range(pageCount):
        page = inputfile.getPage(i)
        page.mergePage(markfile.getPage(0))
        outputfile.addPage(page)
    with open(pdf_file_out, 'wb') as f_out:
        outputfile.write(f_out)

src_folder = Path('/Users/liupan/work/code/seal-python-tools/pdf_process/公告/')
des_folder = Path('/Users/liupan/work/code/seal-python-tools/pdf_process/公告添加水印后/')
if not des_folder.exists():
    des_folder.mkdir(parents=True)
file_list = list(src_folder.glob('*.PDF'))
for pdf in file_list:
    pdf_file_in = str(pdf)
    pdf_file_mark = create_watermark('巨潮资讯网')
    pdf_file_out = str(des_folder / pdf.name)
    add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out)
