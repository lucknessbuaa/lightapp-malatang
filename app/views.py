from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def seatOrder(request):
	return render(request, 'app/seatOrder.html')

def dishes(request):
	return render(request, 'app/dishes.html')

def order(request):
	return render(request, 'app/order.html')

def myOrder(request):
	return render(request, 'app/myOrder.html')