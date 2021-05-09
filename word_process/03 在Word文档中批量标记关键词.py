#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : file.py
# @Software: PyCharm

import win32com.client as win32
word = win32.gencache.EnsureDispatch('Word.Application')
word.Visible = False
cs = win32.constants
doc = word.Documents.Open('/Users/liupan/work/code/seal-python-tools/word_process/员工考勤管理办法.docx')
keyword_list = ['迟到', '早退', '旷工', '脱岗', '串岗']
color_list = [cs.wdRed, cs.wdGreen, cs.wdBlue, cs.wdYellow, cs.wdPink]
for w, c in zip(keyword_list, color_list):
    word.Options.DefaultHighlightColorIndex = c
    findobj = word.Selection.Find
    findobj.ClearFormatting()
    findobj.Text = w
    findobj.Replacement.ClearFormatting()
    findobj.Replacement.Text = w
    findobj.Replacement.Font.Bold = True
    findobj.Replacement.Font.Italic = True
    findobj.Replacement.Font.Underline = cs.wdUnderlineDouble
    findobj.Replacement.Highlight = True
    findobj.Execute(Replace=cs.wdReplaceAll)
doc.SaveAs('F:\\代码文件\\第5章\\处理后的员工考勤管理办法.docx')
doc.Close()
word.Quit()
