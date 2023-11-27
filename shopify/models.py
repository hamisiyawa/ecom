from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    product_title = models.CharField(max_length=30, null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    description = models.CharField(max_length=255,null=True)
    sizes = models.CharField(max_length=10, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], null=True, blank=True)
    colors = models.CharField(max_length=20, null=True, blank=True)
    digital = models.BooleanField(default=False,null=True, blank=False)
    trendy = models.BooleanField(default=False,null=True, blank=False)
    image = models.ImageField(upload_to='media/', default='profile.png')

    def __str__(self):
        return self.product_title


    #  correcting image error when an image is deleted in other products
    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except Exception as e:
            print(f"Error accessing image URL: {e}")
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping_details(self):
        shipping_details = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping_details = True
        return shipping_details



    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



    # @property
    # def get_total_payment(self):
    #     orderitems = self.orderitem_set.all()
    #     total = sum([item.get_total for item in orderitems])
    #     return total

class Shipping(models.Model):
    shipping_cost = models.FloatField(default=0)
    
    def __str__(self):
      return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    mobile = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address


class homeCaurosel(models.Model):
    text1 = models.CharField(max_length=200, null=True)
    text2 = models.CharField(max_length=200, null=True)
    btn_text = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='media/', default='profile.png')

    def __str__(self):
       return str(self.id)


class homeCollections(models.Model):
    heading1 = models.CharField(max_length=200, null=True)
    heading2 = models.CharField(max_length=200, null=True)
    btn_text = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='media/', default='profile.png')

    def __str__(self):
       return str(self.id)

