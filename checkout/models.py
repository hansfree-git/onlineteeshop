from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.auth.models import User
from catalog_app.models import Product
from accounts.models import UserAddress
from cart.models import CartItem
from cart.cart import *
import decimal



class Order(models.Model):
    """ model class for storing a customer order instance """
    # each individual status
    # SUBMITTED = 1
    # PROCESSED = 2
    # SHIPPED = 3
    # CANCELLED = 4
    # set of possible order statuses
    ORDER_STATUSES = (('SUBMITTED','SUBMITTED'),
                      ('PROCESSED','PROCESSED'),
                      ('SHIPPED','SHIPPED'),
                      ('CANCELLED','CANCELLED'),)
    #order info
    order_id = models.CharField(max_length=20,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    shipping_address=models.ForeignKey(UserAddress,null=True,on_delete=models.CASCADE,related_name='order_shipping_address')
    billing_address=models.ForeignKey(UserAddress,null=True,on_delete=models.CASCADE,related_name='order_billing_address')
    status = models.CharField(max_length=20,choices=ORDER_STATUSES, default='SUBMITTED')
    ip_address = models.GenericIPAddressField() #set blank=True, null=True as default so you can add to database
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    transaction_id = models.CharField(max_length=20)

    
    def __str__(self):
        return 'Order #' + str(self.id)
    
    @property
    def total(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.product.price * item.quantity
        return total

    # calculate the tax total with a rate of 17.5% VAT
    @property
    def tax_total(self): 
        # creates an object with a decimal field
        tax_total=decimal.Decimal('0.00')
        return 0.175 * float(self.total)

    # calculates the final total by adding the sum total to tax total
    @property
    def final_total(self):
        # creates an object with a decimal field
        final_total=decimal.Decimal('0.00')
        return self.total + decimal.Decimal(self.tax_total)
    


class OrderItem(models.Model):
    """ model class for storing each Product instance purchased in each order """
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    order = models.ForeignKey(Order,null=True,on_delete=models.SET_NULL)
    
    @property
    def total(self):
        return self.quantity * self.price
    
    @property
    def name(self):
        return self.product.name
    
    def __str__(self):
        return self.product.name +  str(self.product.id) 
    
    def get_absolute_url(self):
        return self.product.get_absolute_url()
    
    