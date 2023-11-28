import json
from . models import *

# define the reusable function

def cookieCart(request):
    try:
       cart = json.loads(request.COOKIES['cart']) 
    except:
        cart = {}

    print('Cart:', cart)
    # shipping = {'shipping_cost': 0}
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0,'shiping_details': False}
    cartItems = order['get_cart_items']

    # loop through the items in cart
    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            # create an item dictionary that will hold all information about the cart items
            item = {
                'product':{
                    'id': product.id,
                    'product_title': product.product_title,
                    'price': product.price,
                    'image': product.image
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }

            items.append(item)

            if product.digital == False:
                order['shiping_details'] == True
        except:
            pass
    
    return {'cartItems': cartItems,'order': order, 'items': items}


def cartData(request):
    # add items to cart if a customer is authenticated
    if request.user.is_authenticated:
        shipping = Shipping.objects.first()
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        shipping = Shipping.objects.first()
        # load the data stored in the cookie named cart
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems,'order': order, 'items': items, 'shipping': shipping}

def guestOrder(request,data):
    print('User not logged in..')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer,complete=False)

    # iterate through the cookie cart items and save them in the database
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order

