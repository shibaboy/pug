#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import loader, RequestContext
from django.template import RequestContext
from django.shortcuts import render_to_response
from subprocess import *
import MySQLdb, os, sys, httplib, urllib, time, datetime



## default view. 
def default_view(error):
	db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='monitor')
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	check_have = 'select a.id, a.name, a.number, a.email from port_check_customer a where a.removed is null'
	cursor.execute(check_have)
	all_have = cursor.fetchall()
	for i in all_have:
	    port_ip_sql = 'select count(distinct(ip)) ip, count(port) port from port_check_port_info where removed is null and customer_id="%s"'%i['id']
	    cursor.execute(port_ip_sql)
	    result = cursor.fetchall()
	    i['ip'] = result[0]['ip']
	    i['port'] = result[0]['port']

	## for port result
	status_q = 'select a.id, a.name, a.number, a.email, b.ip, b.port, b.status, b.description, b.updated  from port_check_customer a left outer join port_check_port_info b on a.id=b.customer_id where a.removed is null and b.removed is null'
	cursor.execute(status_q)
	status_result = cursor.fetchall()

	for i in status_result:
	    if i['status'] != 'Success':
		i['red'] = 'on'
	    tmp1 = i['updated']
	    if len(str(tmp1)) != 4:
		tmp = i['updated']
		i['updated'] = datetime.datetime.fromtimestamp(tmp)
	if error == 1:
	    return render_to_response('port_check.html', {'name_result':all_have, 'status_result':status_result, 'error':True})
	else:
	    return render_to_response('port_check.html', {'name_result':all_have, 'status_result':status_result})

#def port_check(request):
def port_check(request):
    
    ## for add vip
    if request.GET.get('name') and request.GET.get('email') and request.GET.get('number'):
	name = request.GET['name'].strip().encode('utf8')
	email = request.GET['email'].strip().encode('utf8')
	number = request.GET['number'].strip().encode('utf8')

	## check already have that name on the list
	db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='monitor')
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	check_have = 'select a.id, a.name, a.number from port_check_customer a where a.removed is null'
	cursor.execute(check_have)
	all_have = cursor.fetchall()
	check_has = 0

	for i in all_have:
	    if i['name'] == name:
		check_has = 1
	    else:
		continue
	
	## for new customer.
	if check_has == 0:
	    #db.query("set character_set_connection=utf8;")
            #db.query("set character_set_server=utf8;")
            #db.query("set character_set_client=utf8;")
            #db.query("set character_set_results=utf8;")
	    #db.query("set character_set_database=utf8;")

	    add_sql = 'insert into port_check_customer (name, number, email, created) values ("%s", "%s","%s", "%i")' %(name, number, email, int(time.time()))
	    cursor.execute(add_sql)
	    time.sleep(0.5)
	    return default_view(0)
	else:
	    return default_view(1)
    
    ## for remove vip
    elif request.GET.get('remove'):
	id = request.GET['remove'].strip()
	
	## remove user sql
	db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='monitor')
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	remove_sql1 = 'update port_check_customer set removed="%i" where id="%s"' %(int(time.time()), id)
	cursor.execute(remove_sql1)
	remove_sql2 = 'update port_check_port_info set removed="%i" where customer_id="%s"' %(int(time.time()), id)
	cursor.execute(remove_sql2)

	## default show
	return default_view(0)


    ## for add port & ip
    elif request.GET.get('ip') and request.GET.get('id') and request.GET.get('port') and request.GET.get('type'):
	id = request.GET['id'].strip()
	ip = request.GET['ip'].strip()
	port = request.GET['port'].strip()
	type = request.GET['type']

	## check alreadt has that port.
	db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='monitor')
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	port_sql = 'select * from port_check_port_info where removed is null'
	cursor.execute(port_sql)
	all_port_result = cursor.fetchall()
	check_has = 0
	vip_id_valid = 0
	for i in all_port_result:
		if i['ip'] == ip and i['port'] == port:
		    check_has = 1
		elif str(i['customer_id']) == id:
		    vip_id_valid = 1
		else:
		    continue
		    


	if check_has == 0 and vip_id_valid == 1:
		add_port_sql = 'insert into port_check_port_info (customer_id, ip, port, type) values ("%s", "%s", "%s", "%s")' %(id, ip, port, type)
		cursor.execute(add_port_sql)
	else:
	    return default_view(1)

	## default show
	return default_view(0)

    ## base
    else:
	return default_view(0)
	

#def user_info(request):
def user_info(request):
    db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='monitor')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    if request.GET.get('id'):
	user_id = request.GET['id']
	search_user = 'select a.id, a.name, a.number, a.email, b.id port_id, b.ip, b.port, b.status, b.description, b.updated from port_check_customer a left outer join port_check_port_info b on a.id=b.customer_id where a.removed is null and b.removed is null and a.id="%s"'% user_id
	cursor.execute(search_user)
	user_result = cursor.fetchall()
	
	for i in user_result:
	    if i['status'] != 'Success':
		i['red'] = 'on'
	    tmp1 = i['updated']
	    if len(str(tmp1)) != 4:
		tmp = i['updated']
		i['updated'] = datetime.datetime.fromtimestamp(tmp)

	return render_to_response('user_info.html', {'user_result':user_result})
    
    if request.GET.get('port_id'):
	del_port = request.GET['port_id']
	del_port_q = 'update port_check_port_info set removed=%s where id=%s'%(int(time.time()), del_port)
	cursor.execute(del_port_q)
	
	## default_view for user_info
	search_user_before = 'select customer_id from port_check_port_info where id="%s"'% del_port
	cursor.execute(search_user_before)
	user_result_before = cursor.fetchall()

	
	search_user = 'select a.id, a.name, a.number, a.email, b.id port_id, b.ip, b.port, b.status, b.description, b.updated from port_check_customer a left outer join port_check_port_info b on a.id=b.customer_id where a.removed is null and b.removed is null and a.id="%s"'% user_result_before[0]['customer_id']
	cursor.execute(search_user)
	user_result = cursor.fetchall()
	for i in user_result:
	    if i['status'] != 'Success':
		i['red'] = 'on'
	    tmp1 = i['updated']
	    if len(str(tmp1)) != 4:
		tmp = i['updated']
		i['updated'] = datetime.datetime.fromtimestamp(tmp)

	return render_to_response('user_info.html', {'user_result':user_result})

	

    else:
	return default_view(1)

    
def port_check_status(request):
    db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='monitor')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    ## for username
    check_have = 'select a.id, a.name, a.number, a.email from port_check_customer a where a.removed is null'
    cursor.execute(check_have)
    all_have = cursor.fetchall()
    for i in all_have:
	port_ip_sql = 'select count(distinct(ip)) ip, count(port) port from port_check_port_info where customer_id="%s"'%i['id']
	cursor.execute(port_ip_sql)
	result = cursor.fetchall()
	i['ip'] = result[0]['ip']
	i['port'] = result[0]['port']

    ## for port result
    status_q = 'select a.id, a.name, a.number, a.email, b.ip, b.port, b.status, b.description, b.updated  from port_check_customer a left outer join port_check_port_info b on a.id=b.customer_id where a.removed is null'
    cursor.execute(status_q)
    status_result = cursor.fetchall()

    for i in status_result:
	if i['status'] != 'Success':
	    i['red'] = 'on'
	tmp1 = i['updated']
	if len(str(tmp1)) != 4:
	    tmp = i['updated']
	    i['updated'] = datetime.datetime.fromtimestamp(tmp)

    return render_to_response('port_check_status.html', {'name_result':all_have, 'status_result':status_result})



