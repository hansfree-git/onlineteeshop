from django.contrib import admin
from .models import Order,OrderItem

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__','date','status','transaction_id','user')
    list_filter = ('status','date')
    search_fields = ('shipping_name','billing_name','id','transaction_id')
    inlines = [OrderItemInline,]
    
admin.site.register(Order, OrderAdmin)