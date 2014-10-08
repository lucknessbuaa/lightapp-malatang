from django.http import HttpResponse
from django.shortcuts import render, redirect
from backend.models import *
from datetime import timedelta, datetime
from binascii import hexlify
import re, random, json, requests, uuid, os

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def login(request):
	identification = request.COOKIES.get('uuid')
	if identification:
		user = User.objects.filter(identification=identification)[:1]
		if user:
			return redirect('/')

	return render(request, 'app/login.html')

def seatOrder(request):
	identification = request.COOKIES.get('uuid')
	if identification:
		user = User.objects.filter(identification=identification)[:1]
		if not user:
			return redirect('/app/login')
		else:
			user_id = user[0].id
	else:
		return redirect('/app/login')

	request.META["CSRF_COOKIE_USED"] = True
	if request.POST:
		if len(request.POST) == 1 and request.POST.get('mobile', ''):
			mobile = request.POST.get('mobile')
			if re.match(r'^\d{11}$',mobile):
				Verification.objects.filter(mobile=mobile).update(usable=False)
				code = ''.join(random.choice("1234567890") for _ in range(6))
				time = datetime.now() + timedelta(seconds=600)
				Verification.objects.create(time=time, mobile=mobile, code=code)
				#################### mobile message !! ####################
				return HttpResponse(0)
			else:
				return HttpResponse(-1)
		else:
			date = request.POST.get('date','')
			contact = request.POST.get('contact','')
			mobile = request.POST.get('mobile','')
			code = request.POST.get('code','')
			number = request.POST.get('number','')
			if date and contact and re.match(r'^\d{11}$',mobile) and code.isnumeric() and number.isnumeric():
				try:
					verification = Verification.objects.get(mobile=mobile,code=code,usable=True)
					verification.usable = False
					verification.save()
					if datetime.now() > verification.time:
						# outdate
						return HttpResponse(-3)
					else:
						try:
							now = datetime.datetime()
							SeatOrder.objects.filter(now>end).update(usable=True)

							ticket = hexlify(os.urandom(4))
							order = SeatOrder.objects.create(user_id=user_id, date=date, contact=contact, mobile=mobile, number=number, ticket=ticket)
							#################### mobile message !! ####################
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

def orderItem(request):
	identification = request.COOKIES.get('uuid')
	if identification:
		user = User.objects.filter(identification=identification)[:1]
		if not user:
			return redirect('/app/login')
		else:
			user_id = user[0].id
	else:
		return redirect('/app/login')

	dishes = Dishes.objects.filter(removed=False)
	return render(request, 'app/orderItem.html', {'dishes':dishes})

def order(request):
	identification = request.COOKIES.get('uuid')
	if identification:
		user = User.objects.filter(identification=identification)[:1]
		if not user:
			return redirect('/app/login')
		else:
			user_id = user[0].id
	else:
		return redirect('/app/login')

	request.META["CSRF_COOKIE_USED"] = True
	if request.POST:
		if len(request.POST) == 1 and request.POST.get('mobile', ''):
			mobile = request.POST.get('mobile')
			if re.match(r'^\d{11}$',mobile):
				Verification.objects.filter(mobile=mobile).update(usable=False)
				code = ''.join(random.choice("1234567890") for _ in range(6))
				time = datetime.now() + timedelta(seconds=600)
				Verification.objects.create(time=time, mobile=mobile, code=code)
				#################### mobile message !! ####################
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
			if deadline and location and contact and re.match(r'^\d{11}$',mobile) and code.isnumeric() and number.isnumeric() and items:
				try:
					verification = Verification.objects.get(mobile=mobile,code=code,usable=True)
					verification.usable = False
					verification.save()
					if datetime.now() > verification.time:
						# outdate
						return HttpResponse(-3)
					else:
						try:
							items = json.loads(items)
							if not items:
								# no selection
								return HttpResponse(-4)
							############# modify the deadline !! ############
							deadline = datetime.now()
							count = 0
							total = 0
							order = Order.objects.create(user_id=user_id, deadline=deadline, location=location, contact=contact, mobile=mobile, number=number,count=0,total=0)
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

def myOrder(request):
	identification = request.COOKIES.get('uuid')
	if identification:
		user = User.objects.filter(identification=identification)[:1]
		if not user:
			return redirect('/app/login')
		else:
			user_id = user[0].id
	else:
		return redirect('/app/login')

	orders = Order.objects.filter(user_id=user_id).order_by('-date')
	for order in orders:
		items = OrderItem.objects.filter(order_id=order.id)
		order.items = items
	return render(request, 'app/myOrder.html', {'orders':orders})

def auth(request, authType='baidu'):
	code = request.GET.get('code','')
	if authType == 'baidu':
		authType = authType.upper()
		grant_type = 'authorization_code'
		client_id = 'PMQTgEz4V3IerHkX4lfvVh55'
		client_secret = 'dRdXrBFN2s2mzFr3T8BRxMnRRh7Plome'
		redirect_uri = 'http%3A%2F%2Fxa.limijiaoyin.com%2Fapp%2Fauth%2Fbaidu'
		url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type='+grant_type+'&code='+code+'&client_id='+client_id+'&client_secret='+client_secret+'&redirect_uri='+redirect_uri
		try:
			r = requests.get(url)
			ret = json.loads(r.content)
			if 'error' in ret:
				return redirect('/app/login')
			else:
				token = ret['access_token']
				refreshToken = ret['refresh_token']
				rq = requests.get('https://openapi.baidu.com/rest/2.0/passport/users/getLoggedInUser?access_token='+token)
				retn = json.loads(rq.content)
				if 'error_code' in retn:
					return redirect('/app/login')
				else:
					authID = retn['uid']
					identification = str(uuid.uuid1()) + '-' + hexlify(os.urandom(8))
					User.objects.update_or_create(authType=authType, authID=authID, defaults={'authToken':token,'authRefreshToken':refreshToken,'identification':identification})
					response = redirect('/')
					response.set_cookie('uuid', identification, max_age=365*24*60*60)
					return response
		except:
			return redirect('/app/login')

	return HttpResponse(0)