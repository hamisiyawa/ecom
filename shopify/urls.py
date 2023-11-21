from django.urls import path
from . import views

app_name = 'shopify'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('details/', views.details, name='detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin')
]