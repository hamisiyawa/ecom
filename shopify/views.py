from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import *


# Create your views here.
def home(request):
    context = {
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
        shipping = Shipping.objects.first()
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        shipping = {'shipping_cost': 0}
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    
    context = {
     'items':items,
     'order': order,
     'shipping': shipping,
     'name':'cart' }
    return render(request, 'cart.html',context)

def checkout(request):
    # add items to cart if a customer is authenticated
    if request.user.is_authenticated:
        shipping = Shipping.objects.first()
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        shipping = {'shipping_cost': 0}
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {
        'items':items,
        'order': order,
        'shipping': shipping,
        'name':'checkout'
    }

    return render(request, 'checkout.html',context)

def contact(request):
    return render(request, 'contact.html', {'name':'checkout'})

def signin(request):
    return render(request, 'signin.html', {'name':'signin'})

def register(request):
    return render(request, 'register.html', {'name':'register'})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity + 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('item was added', safe=False)