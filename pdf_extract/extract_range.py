#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/3 上午10:22
# @Author  : liupan
# @Site    : 
# @File    : extract_range.py
# @Software: PyCharm
import os

from PyPDF2 import PdfFileReader, PdfFileWriter


def extract_range(file_name, full_name, split_range, output_dir):
    # 转化为PDF文件对象
    pdfFileObj = PdfFileReader(full_name)

    split_pages = split_range.split(',')
    for split_page in split_pages:
        page_range = split_page.split('-')
        page_start = int(page_range[0])
        page_end = int(page_range[1])

        # 利用PyPDF2创建新的Pdf Writer
        pdfWriter = PdfFileWriter()

        for page_num in range(page_start, page_end + 1):
            # pdf文档页码对象编码是从0开始，所以减一
            page_index = int(page_num) - 1

            # 利用PyPDF2提取页码对象
            pageObj = pdfFileObj.getPage(page_index)  # 从0编码

            # 添加已读取的页面对象
            pdfWriter.addPage(pageObj)

        # Extracted pdf file path
        pdf_file_path = os.path.join(output_dir, file_name + '-页面-{}-{}.pdf'.format(page_start, page_end))

        with open(pdf_file_path, 'wb') as pdfOutputFile:
            pdfWriter.write(pdfOutputFile)


def start():
    split_range_list = [
        '2-20,21-23,24-26,27-32,33-38,39-42,43-49'
    ]

    pdf_dir = '/Users/panliu/Downloads/自治区政府公报'
    output_dir = '/Users/panliu/Downloads/自治区政府公报提取页面输出'
    if os.path.isdir(pdf_dir):
        i = 0
        for s in os.listdir(pdf_dir):
            file_name = s[:-4]
            full_name = os.path.join(pdf_dir, s)
            extract_range(file_name, full_name, split_range_list[i], output_dir)
            i = i + 1


if __name__ == '__main__':
    start()
