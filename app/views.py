from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from backend.models import *
from app.utils import *
from django.contrib.auth import authenticate, login as _login
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
from binascii import hexlify
from threading import Lock
import re, random, json, requests, uuid, os

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def login(request):
	if request.user and request.user.is_active:
		return redirect('/')
	content = {
		'baidu_uri':settings.BAIDU_URI,
		'weibo_uri':settings.WEIBO_URI,
		'qq_uri':settings.QQ_URI
	}
	return render(request, 'app/login.html', content)

@login_required()
def seatOrder(request):
	request.META["CSRF_COOKIE_USED"] = True
	if request.POST:
		if len(request.POST) == 1 and request.POST.get('mobile', ''):
			mobile = request.POST.get('mobile')
			if re.match(r'^\d{11}$',mobile):
				Verification.objects.filter(mobile=mobile).update(usable=False)
				code = ''.join(random.choice("1234567890") for _ in range(6))
				time = datetime.now() + timedelta(seconds=600)
				Verification.objects.create(time=time, mobile=mobile, code=code)
				sendCode(mobile,code)
				return HttpResponse(0)
			else:
				return HttpResponse(-1)
		else:
			date = request.POST.get('date','')
			contact = request.POST.get('contact','')
			mobile = request.POST.get('mobile','')
			code = request.POST.get('code','')
			number = request.POST.get('number','')


			date = parseDatetime(date)
			if not date:
				# time format error
				return HttpResponse(-4)
			delta = timedelta(hours=3)
			endDate = date + delta

			if date and contact and re.match(r'^\d{11}$',mobile) and code.isnumeric() and number.isnumeric():
				try:
					verification = Verification.objects.get(mobile=mobile,code=code,usable=True)
					verification.usable = False
					verification.save()
					if datetime.now() > verification.time:
						# outdated
						return HttpResponse(-3)
					else:
						lock = Lock()
						lock.acquire()
						try:
							ret = -1
							now = datetime.now()
							used = SeatOrderItem.objects.filter(ended=False,end__lt=now)
							exclude = []
							for item in used:
								item.ended = True
								try:
									seat = Seat.objects.get(id=item.seat_id)
									seat.ordered -= 1
									if seat.ordered < 0:
										seat.ordered = 0L
									seat.save()
									item.save()
								except Exception, e:
									raise e

							useless = SeatOrderItem.objects.filter(ended=False,start__lte=endDate,end__gte=date).values('seat_id').distinct()
							for item in useless:
								exclude.append(item['seat_id'])

							allSeats = Seat.objects.filter(reserved=False).count()
							available = allSeats - len(useless)
							if available < int(number):
								# not enough seats
								ret = -5
							else:
								ticket = hexlify(os.urandom(4))
								order = SeatOrder.objects.create(user=request.user, date=date, contact=contact, mobile=mobile, number=number, ticket=ticket)
								toUse = Seat.objects.filter(reserved=False).exclude(id__in=exclude).order_by('-ordered')[:number]
								for item in toUse:
									item.ordered += 1
									item.save()
									SeatOrderItem.objects.create(seat_id=item.id,seatOrder_id=order.id,start=date,end=endDate)
								ret = ticket
								#################### mobile message !! ####################
						except Exception, e:
							# common error
							if order:
								order.delete()
							ret = -1
						finally:
							lock.release()
							return HttpResponse(ret)
				except Exception, e:
					# verify error
					return HttpResponse(-2)
			else:
				# common error
				return HttpResponse(-1)

	return render(request, 'app/seatOrder.html')

def dishes(request, page=0):
	page = int(page) if page else 0
	perpage = 4
	count = Dishes.objects.filter(removed=False).count()
	start = page*perpage
	end = start + perpage
	dishes = Dishes.objects.filter(removed=False)[start:end]
	more = page+1 if end<count else 0
	return render(request, 'app/dishes.html', {'dishes':dishes, 'more':more})

@login_required()
def orderItem(request):
	request.META["CSRF_COOKIE_USED"] = True
	dishes = Dishes.objects.filter(removed=False)
	return render(request, 'app/orderItem.html', {'dishes':dishes})

@login_required()
def order(request):
	request.META["CSRF_COOKIE_USED"] = True
	
	if request.POST:
		if len(request.POST) == 1 and request.POST.get('mobile', ''):
			mobile = request.POST.get('mobile')
			if re.match(r'^\d{11}$',mobile):
				Verification.objects.filter(mobile=mobile).update(usable=False)
				code = ''.join(random.choice("1234567890") for _ in range(6))
				time = datetime.now() + timedelta(seconds=600)
				Verification.objects.create(time=time, mobile=mobile, code=code)
				sendCode(mobile,code)
				return HttpResponse(0)
			else:
				return HttpResponse(-1)
		else:
			deadline = request.POST.get('deadline','')
			location = request.POST.get('location','')
			contact = request.POST.get('contact','')
			mobile = request.POST.get('mobile','')
			code = request.POST.get('code','')
			number = request.POST.get('number','')
			items = request.POST.get('items','')

			deadline = parseDatetime(deadline)
			if not deadline:
				# time format error
				return HttpResponse(-6)

			if deadline and location and contact and re.match(r'^\d{11}$',mobile) and code.isnumeric() and number.isnumeric() and items:
				try:
					verification = Verification.objects.get(mobile=mobile,code=code,usable=True)
					verification.usable = False
					verification.save()
					if datetime.now() > verification.time:
						# outdated
						return HttpResponse(-3)
					else:
						try:
							items = json.loads(items)
							if not items:
								# no selection
								return HttpResponse(-4)

							count = 0
							total = 0
							order = Order.objects.create(user=request.user, deadline=deadline, location=location, contact=contact, mobile=mobile, number=number,count=0,total=0)
							for k, v in items.iteritems():
								k = int(k)
								count += v
								try:
									dish = Dishes.objects.get(id=k,removed=False)
								except:
									# the dish was removed
									order.delete()
									return HttpResponse(-5)
								price = dish.price * v
								total += price
								OrderItem.objects.create(dish_id=k,order_id=order.id,count=v,name=dish.name,price=price)
							order.count = count
							order.total = total
							order.save()
							return HttpResponse(order.id)
						except Exception, e:
							# common error
							if order:
								order.delete()
							return HttpResponse(-1)
				except Exception, e:
					# verify error
					return HttpResponse(-2)
			else:
				# common error
				return HttpResponse(-1)
	return render(request, 'app/order.html')

@login_required()
def myOrder(request):
	orders = Order.objects.filter(user=request.user).order_by('-date')
	for order in orders:
		items = OrderItem.objects.filter(order_id=order.id)
		order.items = items
	return render(request, 'app/myOrder.html', {'orders':orders})

@login_required()
def orderComplete(request):
	order = request.GET.get('order','0')
	try:
		now = datetime.now()
		Order.objects.get(id=order,user=request.user,deadline__gt=now)
	except Exception, e:
		return redirect('/')

	items = OrderItem.objects.filter(order_id=order).values('name')[:3]
	return render(request, 'app/orderComplete.html', {'items':items})

def auth(request, authType='baidu'):
	code = request.GET.get('code','')
	if authType == 'baidu':
		try:
			r = requests.get('https://openapi.baidu.com/oauth/2.0/token', params = {
				'grant_type': 'authorization_code',
			    'code': code,
			    'client_id': settings.BD_CLIENT_ID,
			    'client_secret': settings.BD_CLIENT_SECRET,
			    'redirect_uri': settings.BD_REDIRECT_URI
			})
			ret = json.loads(r.content)
			if 'access_token' not in ret:
				return redirect('/app/login')
			else:
				token = ret['access_token']
				user = authenticate(token=token)
				if user is not None:
					_login(request, user)
				else:
					return redirect('/app/login')
		except:
			return redirect('/app/login')
	elif authType == 'weibo':
		try:
			r = requests.post('https://api.weibo.com/oauth2/access_token', data = {
				'grant_type': 'authorization_code',
			    'code': code,
			    'client_id': settings.WB_CLIENT_ID,
			    'client_secret': settings.WB_CLIENT_SECRET,
			    'redirect_uri': settings.WB_REDIRECT_URI
			})
			ret = json.loads(r.content)
			if 'access_token' not in ret:
				return redirect('/app/login')
			else:
				token = ret['access_token']
				user = authenticate(token=token)
				if user is not None:
					_login(request, user)
				else:
					return redirect('/app/login')
		except:
			return redirect('/app/login')
	elif authType == 'qq':
		try:
			r = requests.get('https://graph.qq.com/oauth2.0/token', params = {
				'grant_type': 'authorization_code',
			    'code': code,
			    'client_id': settings.QQ_CLIENT_ID,
			    'client_secret': settings.QQ_CLIENT_SECRET,
			    'redirect_uri': settings.QQ_REDIRECT_URI
			})
			try:
				ret = json.loads(re.search('\{.*\}',r.content).group())
			except Exception, e:
				ret = {x.split('=')[0]:str(x.split('=')[1]) for x in r.content.split("&")}
			
			if 'access_token' not in ret:
				return redirect('/app/login')
			else:
				token = ret['access_token']
				user = authenticate(token=token)
				if user is not None:
					_login(request, user)
				else:
					return redirect('/app/login')
		except:
			return redirect('/app/login')

	return redirect('/')