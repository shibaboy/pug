#!/usr/bin/python
#
# User VM Port Checker v 0.1 
#
# by shibaboy
#

import socket, time, sys, MySQLdb, datetime
import Queue
import threading
from subprocess import *
import alert_email


class Port_master(threading.Thread):
    def __init__(self, customer_id, ip, port, type, email, number):
	threading.Thread.__init__(self)
	self.customer_id = customer_id
	self.ip = ip
	self.port = port
	self.type = type
	self.email = email
	self.number = number

    def run(self):
	db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='monitor')
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	if self.type == 'tcp':
	    try:
		    checker_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		    checker_tcp.settimeout(3.0)
		    checker_tcp.connect((self.ip, int(self.port)))
		    checker_tcp.shutdown(2)
		    print self.ip, self.port, self.type, 'good'
		    success_q = 'update port_check_port_info set status="Success", updated="%s", description="good" where ip="%s" and port="%s" and type="%s"'%(time.time(), self.ip, self.port, self.type)
		    cursor.execute(success_q)
	    except Exception, e:
		    print self.ip, self.port, self.type, e
		    fail_q = 'update port_check_port_info set status="Fail", updated="%s", description="%s" where ip="%s" and port="%s" and type="%s"'%(time.time(), e, self.ip, self.port, self.type)
		    print fail_q
		    cursor.execute(fail_q)
		    alert_email.alert(self.email, self.ip, self.port, e)

	elif type == 'udp':
	    try:
		    checker_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		    checker_udp.settimeout(3.0)
		    checker_udp.connect((self.ip, int(self.port)))
		    checker_udp.shutdown(2)
		    print self.ip, self.port, self.type, 'good'
		    success_q = 'update port_check_port_info set status="Success", updated="%s", description="good" where ip="%s" and port="%s" and type="%s"'%(time.time(), self.ip, self.port, self.type)
		    cursor.execute(success_q)
	    except Exception, e:
		    print self.ip, self.port, self.type, e
		    fail_q = 'update port_check_port_info set status="Fail", updated="%s", description="%s" where ip="%s", port="%s", type="%s"'%(time.time(), e, self.ip, self.port, self.type)
		    cursor.execute(fail_q)
		    alert_email.alert(self.email, self.ip, self.port, e)

	else:
	    print 'type is unknown'
	    fail_qq = 'update port_check_port_info set status="Fail", updated="%s", description="unknown_type" where ip="%s" and port="%s" and type="%s"'%(time.time(), self.ip, self.port, self.type)
	    cursor.execute(fail_qq)
	    alert_email.alert('shibaboy@gmail.com', self.ip, self.port,'check_ip')

def Commander():

    ## print current time
    print '==== ',datetime.datetime.now(), ' ===='

    ## search DB for customer ip, port, type
    db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='monitor')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    search_query = 'select a.customer_id, a.ip, a.port, a.type, b.email, b.number from port_check_port_info a, port_check_customer b where a.customer_id=b.id and b.removed is null and a.removed is null'
    cursor.execute(search_query)
    search_result = cursor.fetchall()


    ## check status of searched port, ip
    for check in search_result:
	start = Port_master(check['customer_id'], check['ip'], check['port'], check['type'], check['email'], check['number'])
	start.start()


if __name__ == '__main__':
    Commander()
