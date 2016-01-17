# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年10月20日 星期二 13时30分52秒
#
'''
    发送邮件文件
'''
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import config
import smtplib
import tornado.gen
import tornado_email.client as async_smtp


def deal_with_address(declare_name, address):
    return formataddr(
        (
            Header(declare_name, 'utf-8').encode(),
            address.encode('utf-8'),
        )
    )


def send(
    title=None,
    message=None,
    host=config.Config.MAIL_SERVER,
    user=config.Config.MAIL_USER,
    password=config.Config.MAIL_PASSWD,
    to=config.Config.MAIL_TO,
    callback=None,
):
    server = smtplib.SMTP()
    server.connect(host)
    server.starttls()
    server.login(user, password)
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = deal_with_address(u'武汉大学互联网数据挖掘实验室', user)
    msg['Subject'] = Header(title, 'utf-8').encode()
    to_addrs = [to_addr.encode('utf-8') for to_addr in to.split('|')]
    msg['To'] = ', '.join(to_addrs)
    server.sendmail(user, to_addrs, msg.as_string())
    server.quit()


@tornado.gen.coroutine
def async_send(
    title=None,
    message=None,
    host=config.Config.MAIL_SERVER,
    user=config.Config.MAIL_USER,
    password=config.Config.MAIL_PASSWD,
    to=config.Config.MAIL_TO,
    callback=None,
):
    server = async_smtp.AsyncSMTP()
    yield server.connect(host=host)
    yield server.start_tls()
    yield server.login(username=user, password=password)
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = deal_with_address(u'武汉大学互联网数据挖掘实验室', user)
    msg['Subject'] = Header(title, 'utf-8').encode()
    to_addrs = [to_addr.encode('utf-8') for to_addr in to.split('|')]
    msg['To'] = ', '.join(to_addrs)
    yield server.send_mail(user, to_addrs, msg.as_string())
    yield server.quit()
