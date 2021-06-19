#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/27 12:14 下午
# @Author  : silianpan
# @Site    : pdf逐页输出图片
# @File    : pdf2img.py
# @Software: PyCharm

import fitz
import os
import datetime


def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.writePNG(imagePath + '/' + '北斗_%s.png' % pg)  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)


def pyMuPDF2_fitz(pdfPath, imagePath):
    pdfDoc = fitz.open(pdfPath)  # open document
    for pg in range(pdfDoc.pageCount):  # iterate through the pages
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)  # 缩放系数1.3在每个维度  .preRotate(rotate)是执行一个旋转
        rect = page.rect  # 页面大小
        mp = rect.tl + (rect.bl - (0, 75 / zoom_x))  # 矩形区域    56=75/1.3333
        clip = fitz.Rect(mp, rect.br)  # 想要截取的区域
        pix = page.getPixmap(matrix=mat, alpha=False, clip=clip)  # 将页面转换为图像
        if not os.path.exists(imagePath):
            os.makedirs(imagePath)
        pix.writePNG(imagePath + '/' + 'psReport_%s.png' % pg)  # store image as a PNG


if __name__ == "__main__":
    pdfPath = r'/Users/liupan/Downloads/uploadPath/input/test.pdf'
    imagePath = '/Users/liupan/Downloads/uploadPath/output'
    # pyMuPDF_fitz(pdfPath, imagePath)#只是转换图片
    pyMuPDF_fitz(pdfPath, imagePath)  # 指定想要的区域转换成图片
