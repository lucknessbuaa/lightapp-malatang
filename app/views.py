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
	count = Dishes.objects.count()
	start = page*perpage
	end = start + perpage
	dishes = Dishes.objects.all()[start:end]
	more = page+1 if len(dishes) else 0
	return render(request, 'app/dishes.html', {'dishes':dishes, 'more':more})

def order(request):
	return render(request, 'app/order.html')

def myOrder(request):
	return render(request, 'app/myOrder.html')