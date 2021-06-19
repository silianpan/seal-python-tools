#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : file.py
# @Software: PyCharm

import smtplib
import pandas as pd
from email.mime.text import MIMEText
user = '***@qq.com'
code = 'thoh****vbbb****'
data = pd.read_excel('客户资料统计表.xlsx', sheet_name=0)
e_mail = data['联系人邮箱'].tolist()
to = ','.join(e_mail)
message = MIMEText('邮件正文内容')
message['Subject'] = '邮件主题'
message['From'] = user
message['To'] = to
server = smtplib.SMTP_SSL('smtp.qq.com', 465)
server.login(user, code)
server.send_message(message)
server.quit()
print('邮件发送成功！')
