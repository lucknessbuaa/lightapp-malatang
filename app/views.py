from django.http import HttpResponse
from django.shortcuts import render
from backend.models import *
from datetime import timedelta, datetime
import re
import random
import json

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def login(request):
	return render(request, 'app/login.html')

def seatOrder(request):
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
	dishes = Dishes.objects.filter(removed=False)
	return render(request, 'app/orderItem.html', {'dishes':dishes})

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
			if re.match(r'^\d{11}$',mobile) and code.isnumeric() and number.isnumeric():
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
							order = Order.objects.create(user_id=1, deadline=deadline, location=location, contact=contact, mobile=mobile, number=number,count=0,total=0)
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
	# fake
	orders = Order.objects.filter(user_id=1).order_by('-date')
	for order in orders:
		items = OrderItem.objects.filter(order_id=order.id)
		order.items = items
	return render(request, 'app/myOrder.html', {'orders':orders})