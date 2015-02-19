#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import requests
import time
import logging
import re
from requests.auth import HTTPBasicAuth
from sys import argv
import uptimer

general_user = 'tianle1218'
general_passwd = 'secworld'
IP = ''

#----------------------------system config-------------------------------------
interval = 60.0
listen_timeout = 3.0
logpath = './update.log'
#______________________________________________________________________________	

def set_loglevel(argv):
	if len(argv) == 2 and argv[1] == '-v':
		logger.setLevel(logging.DEBUG)
				
	else :
		logger.setLevel(logging.INFO)

logger = logging.getLogger('ddns')
set_loglevel(argv)

fh = logging.FileHandler(logpath)
fh.setLevel(logging.DEBUG)

format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') 
fh.setFormatter(format)
logger.addHandler(fh)

def params_proc_general(params, conf):
	params['hostname'] = conf['hostname']
	params['myip'] = getip()

def params_proc_pubyun(params, conf):
	'''
	params参数处理,pubyun进行requests调用
	'''
	params['hostname'] = conf['hostname']
	params['myip'] = getip()
	params['wildcard'] = 'OFF'
	params['mx'] = 'mail.exchanger.ext'
	params['backmx'] = 'NO'
	params['offline'] = 'NO'

def params_proc_dtdns(params, conf):
	params['id'] = conf['hostname']
	params['ip'] = getip()
	params['pw'] = conf['passwd']


class Userconf(object):
	def __init__(self):
		self.enable = False
		self.config = {
			'svr': '',
			'user': '',
			'passwd': '',
			'hostname': '',
		}
	
class Url(object):
	def __init__(self):
		self.url = ''
		self.params = {}


class Updateconf(Userconf, Url):
	def __init__(self):
		Userconf.__init__(self)
		Url.__init__(self)
		self.auth = ''

	def params_proc(self):
		if self.enable:
			if self.config['svr'] == 'oray':
				params_proc_general(self.params, self.config)
			if self.config['svr'] == 'pubyun':
				params_proc_pubyun(self.params, self.config)
			if self.config['svr'] == 'changeip':
				params_proc_general(self.params, self.config)
			if self.config['svr'] == 'noip':
				params_proc_general(self.params, self.config)
			if self.config['svr'] == 'dtdns':
				params_proc_dtdns(self.params, self.config)

	def url_proc(self):
		if self.enable:
			if self.config['svr'] == 'oray':
				self.url = r"http://ddns.oray.com/ph/update" 
			elif self.config['svr'] == 'pubyun':
				self.url = r'http://members.3322.net/dyndns/update' 
			elif self.config['svr'] == 'changeip':
				self.url = r'http://dynupdate.no-ip.com/nic/update' 
			elif self.config['svr'] == 'noip':
				self.url = r'http://dynupdate.no-ip.com/nic/update' 
			elif self.config['svr'] == 'dtdns':
				self.url = r'http://www.dtdns.com/api/autodns.cfm' 
			else:
				pass

	def set_http_auth(self):
		self.auth = HTTPBasicAuth(self.config['user'], self.config['passwd'])

oray = Updateconf()
pubyun = Updateconf()
chgip = Updateconf()
noip = Updateconf()
dtdns = Updateconf()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^user config^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#注意：只有将对应服务商的 enable 值设置为True才能对其更新，例如：oray.enable = True
#设置为False时不进行更新
# ORAY 
oray.enable = False
oray.config['svr'] = 'oray'
oray.config['user'] = '此处填写用户名'
oray.config['passwd'] = '此处填写密码'
oray.config['hostname'] = '此处填写域名'

# pubyun(f3322)
pubyun.enable = False
pubyun.config['svr'] = 'pubyun'
pubyun.config['user'] = '此处填写用户名'
pubyun.config['passwd'] = '此处填写密码'
pubyun.config['hostname'] = '此处填写域名'

# CHANGEIP
chgip.enable = False
chgip.config['svr'] = 'changeip'
chgip.config['user'] = '此处填写用户名'
chgip.config['passwd'] = '此处填写密码'
chgip.config['hostname'] = '此处填写域名'

# NOIP
noip.enable = False
noip.config['svr'] = 'noip'
noip.config['user'] = '此处填写用户名'
noip.config['passwd'] = '此处填写密码'
noip.config['hostname'] = '此处填写域名'

## DTDNS
dtdns.enable = True
dtdns.config['svr'] = 'dtdns'
dtdns.config['user'] = '此处填写用户名'
dtdns.config['passwd'] = '此处填写密码'
dtdns.config['hostname'] = '此处填写域名'
#_____________________________________________________________________________

def conf_init(user_conf):
	global IP
	IP = getip()
	logger.info('IP %s' % IP)

	for conf in user_conf:
		conf.url_proc()
		conf.params_proc()
		conf.set_http_auth()

def getip():
	'''
	根据开放的WEB API获取本地出口的ip地址
	'''
	url = 'http://ip.3322.net/'
	r = requests.get(url)

	m = re.search(r"((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)", r.text)	
	return m.group() 

def response_parse(r):
	logger.debug('%s %s' % (r.status_code, r.text))
	if r.status_code != 200:
		logger.error('Error server response ', r.status_code)
		return fail;
	
	text = r.text
	if ('good' in text) or ('nochg' in text) or ('Successful' in text) or ('now points to' in text):
		logger.info('Successful Update')
	else :
		logger.info('Fail Update')

def update(user_conf):
	for conf in user_conf:
		if conf.enable == False:
			continue
		logger.debug(conf.params)
		if conf.config['svr'] == 'dtdns':
			hostname = conf.params['id']
		else :
			hostname = conf.params['hostname']
		logger.info(hostname)

		r = requests.get(conf.url, params=conf.params, auth=conf.auth)

		response_parse(r)

def listenip(user_conf):
	global IP

	curip = getip()
	if curip == IP:
		logger.debug('IP %s' % IP)
		return
	
	logger.info('IP %s' % IP)
	conf_init(user_conf)
	update(user_conf)

config = [oray, pubyun, chgip, noip, dtdns]

conf_init(config)
update(config)

re_timer = uptimer.RepeatableTimer(interval, update, config)
re_timer.start()

listentimer = uptimer.RepeatableTimer(listen_timeout, listenip, config)
listentimer.start()
