import time
import re
import random
import requests
import urllib3
import json
from urllib import parse
from PIL import Image
from threading import Thread

urllib3.disable_warnings()


def get_time():
    return str(int(time.time()*1000))

def get_DeviceID():
    return 'e'+str(round(random.random(),15))[2:17]

def format_synckey(synckey_list):
    '''
    把列表形式转成查询字符串
    '''
    tem_synckey = ''
    for synckey in synckey_list:
        tem_synckey += str(synckey['Key']) + '_' +str(synckey['Val']) + '|'
    new_synckey = {'synckey':tem_synckey.rstrip('|')}
    return parse.urlencode(new_synckey)

class WeChat():
    def __init__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }  # 请求头信息
        proxies = {
            'http': '192.168.105.71:80',
            'https': '192.168.105.71:80'
        }  # 使用代理
        self.user_list = {}
        self.session = requests.session()
        self.session.headers = headers
        self.session.proxies = proxies
        self.session.verify = False

    def get_uuid(self):
        '''获取uuid'''
        url = 'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={}'.format(get_time())
        response = self.session.get(url).text
        self.uuid = re.findall(r'uuid = "(.*?)"',response)[0] # 文本较少，用正则匹配即可
        return self.uuid

    def qrcode(self):
        url = 'https://login.weixin.qq.com/qrcode/{}'.format(self.uuid)
        response = self.session.get(url).content  # 请求得到二维码，由于是图片，得到字节码即可
        with open ('qrcode.jpg','wb') as f:
            f.write(response)  # 把二维码保存到一张图片里
        im = Image.open('qrcode.jpg')
        im.show()  # 把二维码图片展示出来

    def get_redirect_uri(self):
        while True:  # 由于需要不断请求，让我们有时间来扫描二维码
            url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={}&tip=0&r=-2109595288&_={}'.format(self.uuid,get_time())
            result = self.session.get(url,allow_redirects=False)
            code = re.findall(r'window.code=(.*?);',result.text)[0]
            if code == '200': # 没有扫描的时候是400，扫描之后就是200
                print('已成功扫描二维码！')
                break
        self.redirect_uri = re.findall(r'window.redirect_uri="(.*?)"',result.text)[0] # 得到一个链接，请求之后会得到一些有用的参数

    def get_require_data(self):
        result = self.session.get(self.redirect_uri,allow_redirects=False).text # 这里注意一定要去掉重定向
        print(result)
        self.skey = re.findall(r'<skey>(.*?)</skey>',result)[0]  # 这里用Beautifulsoup也能解析，文本是xml格式的，用匹配标签就可以得到
        self.wxsid = re.findall(r'<wxsid>(.*?)</wxsid>',result)[0]
        self.wxuin = re.findall(r'<wxuin>(.*?)</wxuin>',result)[0]
        self.pass_ticket = re.findall(r'<pass_ticket>(.*?)</pass_ticket>',result)[0]

    def login(self):
        url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-2109580211&pass_ticket={}'.format(self.pass_ticket)
        params = {
            "BaseRequest":{
            "Uin":self.wxuin,
                "Sid":self.wxsid,
                "Skey":self.skey,
                "DeviceID":get_DeviceID(),  # DeviceID这个参数在前面的应答中没有找到，它是js生成的
                            }
                }
        result = self.session.post(url,data=json.dumps(params,ensure_ascii=False))
        result.encoding = 'utf-8'
        data = result.json()
        user = data['User']
        nickname = user['NickName']
        username = user['UserName']
        self.user_list[nickname] = username # 把自己账号的昵称和用户编号保存起来，方便后面收发消息
        self.synckey_list = data['SyncKey']  # synckey 用于后面同步消息
        print('已成功登录!!')
        self.synckey = format_synckey(self.synckey_list['List'])  # 把 synckey构造成查询字符串的模式



    def get_userlist(self):
        '''把用户的好友列表保存起来，方便后面收发消息'''
        url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?pass_ticket={}&r={}&seq=0&skey={}'.format(self.pass_ticket,get_time(),self.skey)
        response = self.session.get(url)
        response.encoding = 'utf-8'
        result = response.json()
        memberlist = result['MemberList']
        for member in memberlist:
            nickname = member['NickName']
            username = member['UserName']
            self.user_list[nickname] = username  # 按照昵称-用户编号的一一对应关系保存

    def get_new_synckey(self):  # 得到最新的synckey 发送或者接收消息后都有这个操作
        url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync?sid={}&skey={}&pass_ticket={}'.format(self.wxsid,self.skey,self.pass_ticket)
        data = {"BaseRequest":{"Uin":self.wxuin,"Sid":self.wxsid,"Skey":self.skey,"DeviceID":get_DeviceID()},"SyncKey":self.synckey_list,"rr":2112925520}
        response = self.session.post(url,data=json.dumps(data,ensure_ascii=False))
        response.encoding = 'utf8'
        result = response.json()
        self.synckey_list = result['SyncKey']
        self.synckey = format_synckey(self.synckey_list['List'])

    def sync_check(self):  # 检查是否有新消息
        while True:
            # 注意这里的synckey是在url里面，所以要进行urlencode，而且synckey改变之后，url也会变，所以url要放在while True里面
            url = 'https://webpush.wx.qq.com/cgi-bin/mmwebwx-bin/synccheck?r={}&skey={}&sid={}&uin={}&deviceid={}&{}'.format(get_time(),self.skey,self.wxsid,self.wxuin,get_DeviceID(),self.synckey)
            response = self.session.get(url)
            response.encoding = 'utf8'
            result = response.text
            # print('正在轮询是否有新消息...')
            selector = re.findall(r'selector:"(.*?)"',result)[0]
            if selector != '0':
                self.get_msg()  # 我这里发消息是在另一个线程，收消息在这个线程
                self.get_new_synckey()  # 每次都需要更新



    def send_msg(self):
        url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?pass_ticket={}'.format(self.pass_ticket)
        while True:
            msg = input('>>>>>')
            if msg == 'q':
                break
            data = {
                "BaseRequest":{
                    "Uin":self.wxuin,
                    "Sid":self.wxsid,
                    "Skey":self.skey,
                    "DeviceID":get_DeviceID()},
                "Msg":{
                    "Type":1,
                    "Content":msg,
                    "FromUserName":self.user_list['xxx'], # 这里填你自己微信昵称
                    "ToUserName":self.user_list['xxx'],  # 这里填你想发送消息的好友的昵称，你也可以用input键盘输入的方式
                    "LocalID":get_time(),
                    "ClientMsgId":get_time()},
                "Scene":0
            }

            self.session.post(url,data=(json.dumps(data,ensure_ascii=False)).encode('utf-8'))
            self.get_new_synckey()  # 发送消息之后也会更新synckey



    def get_msg(self):
        '''接收消息'''
        url = ' https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync?sid={}&skey={}&pass_ticket={}'.format(self.wxsid,self.skey,self.pass_ticket)
        data = {
            "BaseRequest":{
                "Uin":self.wxuin,
                "Sid":self.wxsid,
                "Skey":self.skey,
                "DeviceID":get_DeviceID()},
            "SyncKey":self.synckey_list,
               "rr":-2123282759}
        response = self.session.post(url,data=json.dumps(data))
        response.encoding = 'utf-8'
        result = response.json()
        self.synckey_list = result['SyncKey'] # 接受消息的时候，响应里面有这个值，在更新synckey的时候，参数和响应里都有synckey
        self.synckey = format_synckey(self.synckey_list['List'])
        msglist = result['AddMsgList']
        for msg in msglist:
            if msg['ToUserName'] == self.user_list['XXXX']: # 这里面填你自己微信的昵称，不过加上之后不会受到群消息，大家可以试试不加这个判断
                fromName = msg['FromUserName']
                for k,v in self.user_list.items():
                    if v == fromName:
                        fromNickName = k
                        content = msg['Content']
                        print('来自{}的消息：{}'.format(fromNickName,content))

    def main(self):
        self.get_uuid()
        self.qrcode()
        self.get_redirect_uri()
        self.get_require_data()
        self.login()
        self.get_userlist()
        send_msg = Thread(target=self.send_msg)
        recieve_msg = Thread(target=self.sync_check)
        send_msg.start()
        recieve_msg.start()
        send_msg.join()
        recieve_msg.join()


if __name__ == '__main__':
    wechat = WeChat()
    wechat.main()
