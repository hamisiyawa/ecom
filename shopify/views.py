from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def home(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'name':'home'
    }
    return render(request, 'index.html',context)

def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context ={
        'categories': categories,
        'products': products,
        'name':'shop'
    }
    return render(request, 'shop.html',context)

def details(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'name':'detail'
    }
    return render(request, 'detail.html',context)

def cart(request):
    # add items to cart if a customer is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []

    
    context = {
        'items':items,
        'name':'cart'
    }
    return render(request, 'cart.html',context)

def checkout(request):
    return render(request, 'checkout.html', {'name':'checkout'})

def contact(request):
    return render(request, 'contact.html', {'name':'checkout'})

def signin(request):
    return render(request, 'signin.html', {'name':'signin'})

def register(request):
    return render(request, 'register.html', {'name':'register'})