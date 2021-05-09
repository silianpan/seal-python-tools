#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 上午9:30
# @Author  : silianpan
# @Site    :
# @File    : file.py
# @Software: PyCharm

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
user = '***@qq.com'
code = 'thoh****vbbb****'
to = '****@qq.com'
mail_message = '''
<p>段落内容</p>
<p><a href="https://www.baidu.com">包含链接的段落</a></p>
'''
message = MIMEMultipart()
message.attach(MIMEText(mail_message, 'html', 'utf-8'))
attachment1 = MIMEText(open('/Users/liupan/work/code/seal-python-tools/email_process/table.xlsx', 'rb').read(), 'base64', 'utf-8')
attachment1['Content-Type'] = 'application/octet-stream'
attachment1.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', '统计表1.xlsx'))
message.attach(attachment1)
attachment2 = MIMEText(open('/Users/liupan/work/code/seal-python-tools/email_process/test.xlsx', 'rb').read(), 'base64', 'utf-8')
attachment2['Content-Type'] = 'application/octet-stream'
attachment2.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', '统计表2.xlsx'))
message.attach(attachment2)
message['Subject'] = '邮件主题'
message['From'] = user
message['To'] = to
server = smtplib.SMTP_SSL('smtp.qq.com', 465)
server.login(user, code)
server.send_message(message)
server.quit()
print('邮件发送成功！')


