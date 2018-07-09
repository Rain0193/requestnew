#!/usr/bin/python
#-*- encoding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
class SendEmail:
    def __init__(self,host_dir,email_port,username,passwd):
        self.host_dir=host_dir
        self.email_port=email_port
        self.username=username
        self.passwd=passwd

        self.__connect()
        self.__login()

    #连接邮件服务器
    def __connect(self):
        try:
            self.e = smtplib.SMTP()
            self.e.connect(self.host_dir, port=self.email_port)
            print("邮件服务器连接成功")
        except:
            print ("邮件服务器连接失败")

    #登录邮箱
    def __login(self):
        try:
            self.e.login(self.username, self.passwd)
            print("邮箱登录成功")
        except:
            print ("邮箱登录失败")

    #添加附件
    def __addannex(self,logs):
        for log in logs.keys():
            try:
                textpart = MIMEApplication(open(logs[log], 'rb').read())
                textpart.add_header('Content-Disposition', 'attachment', filename=log+".text")
                self.message.attach(textpart)
            except:
                print (log+" not exist")
    #添加内容
    def add_message(self,html,logs):
        #添加html
        with open(html,'rb') as fp:
            msg_text=fp.read()
            fp.close()
        msg = MIMEText(msg_text, 'html', 'utf-8')
        self.message = MIMEMultipart()
        self.message.attach(msg)

        #添加附件日志
        self.__addannex(logs)


    #添加头部信息
    def add_header(self,headerfrom,headerto,subject):
        self.message['from'] = Header(headerfrom, 'utf-8')
        self.message['to'] = Header(headerto, 'utf-8')
        self.message['Subject'] = Header(subject, 'utf-8')

    #发送邮件
    def send(self,sender,receivers):
        try:
            self.e.sendmail(sender, receivers, self.message.as_string())
            print("邮件发送完成")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")
        finally:
            self.e.quit()

sendemail = SendEmail("smtp.163.com", "25", "nxytest001@163.com", "a1l9e8x6")
filename=r"E:\report18-07-0906-25-33.html"
logs={"successlog":r"E:\Successlog18-07-0809-41-07.text","errorlog":"E:\Errorlog18-06-2112-44-06.text"}
sendemail.add_message(filename, logs)
sendemail.add_header("nxytest001@163.com", "zyq@cheok.com", "测试1")
sendemail.send("nxytest001@163.com", "zyq@cheok.com".split(','))