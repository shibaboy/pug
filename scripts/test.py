#!/usr/bin/python
#
# User VM Port Checker v 0.1 
#
# by shibaboy
#

import socket, time, sys, MySQLdb
import Queue
import threading
import socket
from subprocess import *

#db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='monitor')
#cursor = db.cursor(MySQLdb.cursors.DictCursor)


#ip = '14.63.195.135'
ip = '14.63.253.34'
port = '22'
type = 'tcp'


checker_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
checker_tcp.settimeout(3.0)
checker_tcp.connect((ip, int(port)))
checker_tcp.shutdown(2)
print ip, port, type, 'good'
