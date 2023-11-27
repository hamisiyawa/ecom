from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
import json
from .models import *
import datetime
import random
from . utils import cookieCart, cartData


# Create your views here.
def home(request):
    trendy_products = Product.objects.filter(trendy=True)
    image_caurosels = homeCaurosel.objects.all()
    collections = homeCollections.objects.all()

    # Shuffle the collection items randomly
    shuffled_collections = list(collections)
    random.shuffle(shuffled_collections)
    # Take the first two items
    selected_collections = shuffled_collections[:2]

    # Fetch all categories and their associated products, limit to 6 categories
    categories_with_products = (
        Category.objects.annotate(num_products=Count('product'))
        .filter(num_products__gt=0)
        .prefetch_related('product_set')
        .order_by('?')[:6]
    )

    # get data from utils.py 
    data = cartData(request)
    # shipping = data['shipping']
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {
        'cartItems': cartItems,
        'items':items,
        'order': order,
        'trendy_products': trendy_products,
        'collections': selected_collections,
        'image_caurosels': image_caurosels,
        'categories_with_products': categories_with_products,
        'name':'home',
    }
    return render(request, 'index.html',context)

def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    # get data from utils.py 
    data = cartData(request)
    shipping = data['shipping']
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context ={
        'cartItems': cartItems,
        'items':items,
        'order': order,
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
    # get data from utils.py 
    data = cartData(request)
    shipping = data['shipping']
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {
     'cartItems': cartItems,
     'items':items,
     'order': order,
     'shipping': shipping,
     'name':'cart' }
    return render(request, 'cart.html',context)

def checkout(request):
     # get data from utils.py 
    data = cartData(request)
    shipping = data['shipping']
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'cartItems': cartItems,
        'items':items,
        'order': order,
        'shipping': shipping,
        'name':'checkout'
    }

    return render(request, 'checkout.html',context)

def contact(request):


    # get data from utils.py 
    data = cartData(request)
    cartItems = data['cartItems']

    
    context = {
        'cartItems': cartItems,
        'name':'checkout'
    }
    return render(request, 'contact.html',context )

def signin(request):


    # get data from utils.py 
    data = cartData(request)
    cartItems = data['cartItems']
    
    context = {
        'cartItems': cartItems,
        'name':'signin'
    }
    return render(request, 'signin.html',context)

def register(request):

    # get data from utils.py 
    data = cartData(request)
    cartItems = data['cartItems']
    
    context = {
        'cartItems': cartItems,
        'name':'register'
    }
    return render(request, 'register.html',context )


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
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        order.complete = True
        order.save()

        if order.shipping_details == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                mobile = data['shipping_details']['mobile'],
                address = data['shipping_details']['address'],
                city = data['shipping_details']['city'],
                state = data['shipping_details']['state'],
                zipcode = data['shipping_details']['zipcode'],

            )

    else:
        print('User not logged in..')
    return JsonResponse('payment submited..', safe=False)