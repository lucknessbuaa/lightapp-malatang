from datetime import timedelta, datetime
from backend.models import Account
from django.contrib.auth.models import User

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


def getAccount(user):
	try:
		account = Account.objects.get(user=user)
		return account
	except Exception, e:
		return None