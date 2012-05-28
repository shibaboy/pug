#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# for mail alert to customers. 
#
# by shibaboy

import time, smtplib

def alert(email, ip, port, description):
    sender = 'port_alert@pug.com'
    #receivers = ['joonhyun.pac@kt.com', email]
    receivers = ['joonhyun.pac@kt.com']
    message = '''From: kt ucloud Monitoring Service <port_alert@pug.com>
Subject: IP, Port fail occer
Cannot access below ip and port now. please check your vm status. 

IP : %s
Port : %s
error message : %s
'''% (ip, port, description)
    try:
	smtpObj = smtplib.SMTP('localhost')
	smtpObj.sendmail(sender, receivers, message)
	print 'Sent mail Success'
    except:
	print 'Sent mail Failed'


#alert('shibaboy@gmail.com', '14.63.195.135', '80', 'cannot access')
#if __name__ == '__main__':
#    alert(email, ip, port, description)

