#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/7 下午3:20
# @Author  : liupan
# @Site    : 
# @File    : img2ocr.py
# @Software: PyCharm

from PIL import Image
import pytesseract

image = Image.open('Doc202004071439150008.png')
content = pytesseract.image_to_string(image, lang='chi_sim')  # 解析图片
content = content.replace(' ', '')
print(content)
