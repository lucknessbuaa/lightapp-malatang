from django.shortcuts import render
from backend.models import *

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

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
	return render(request, 'app/order.html')

def myOrder(request):
	# fake
	orders = Order.objects.filter(user_id=1).order_by('-date')
	for order in orders:
		items = OrderItem.objects.filter(order_id=order.id)
		order.items = items
	return render(request, 'app/myOrder.html', {'orders':orders})