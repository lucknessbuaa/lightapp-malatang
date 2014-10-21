# -*- coding: utf-8 -*-  
from datetime import timedelta, datetime
import requests

def parseDatetime(str):
	FORMATS = ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
		'%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
		'%Y-%m-%d',              # '2006-10-25'
		'%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
		'%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
		'%m/%d/%Y',              # '10/25/2006'
		'%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
		'%m/%d/%y %H:%M',        # '10/25/06 14:30'
		'%m/%d/%y']              # '10/25/06'
	now = datetime.now()
	for format in FORMATS:
		try:
			t = datetime.strptime(str,format)
			if t > now:
				return t
			else:
				return 0
		except Exception, e:
			pass
	return 0

def sendCode(mobile,code):
	url = 'http://tui3.com/api/send'
	content = u'尊敬的会员,您的验证码是'+str(code)+u',有效期为10分钟,感谢您使用麻辣烫客户端！'
	r = requests.get(url, params = {
		'k':'6e91b7636ae753da4b9596153965e94d',
		'r':'json',
		'p':'1',
		't':mobile,
		'c':content
	})
	print r.content