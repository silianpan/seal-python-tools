#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/3 上午10:22
# @Author  : liupan
# @Site    : 
# @File    : extract_range.py
# @Software: PyCharm
import os

from PyPDF2 import PdfFileReader, PdfFileWriter


def extract_range(full_name, split_range, output_dir):
    # 转化为PDF文件对象
    pdfFileObj = PdfFileReader(full_name)

    split_pages = split_range['page'].split(',')
    i = 0
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
        pdf_file_path = os.path.join(output_dir, split_range['text'][i] + '-{}-{}.pdf'.format(page_start, page_end))
        i = i + 1

        with open(pdf_file_path, 'wb') as pdfOutputFile:
            pdfWriter.write(pdfOutputFile)


def start():
    split_range_list = [
        {
            'page': '2-20,21-23,24-26,27-32,33-38,39-42,43-49',
            'text': [
                '2018年政府工作报告',
                '西藏自治区人民政府关于废止和宣布失效部分规范性文件的决定',
                '西藏自治区人民政府办公厅关于严格控制新设行政许可的通知',
                '西藏自治区人民政府办公厅印发关于推进农业水价综合改革实施方案的通知',
                '西藏自治区人民政府办公厅关于印发西藏自治区推进“互联网+政务服务”实施方案的通知',
                '西藏自治区人民政府办公厅关于印发推进全区城镇人口密集区危险化学品生产企业搬迁改造工作实施方案的通知',
                '政府定价经营服务性收费目录清单'
            ]
        }
    ]

    pdf_dir = './input'
    output_dir = './output'
    if os.path.isdir(pdf_dir):
        i = 0
        for s in os.listdir(pdf_dir):
            # file_name = s[:-4]
            full_name = os.path.join(pdf_dir, s)
            extract_range(full_name, split_range_list[i], output_dir)
            i = i + 1


if __name__ == '__main__':
    start()
