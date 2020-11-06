from django.contrib import admin

# Register your models here.
from.models import UserStripe, UserAddress, UserDefaultAddress

admin.site.register(UserStripe)
admin.site.register(UserDefaultAddress)

class UserAddressAdmin(admin.ModelAdmin):
	list_filter = ('shipping_name','user','shipping_country')

admin.site.register(UserAddress,UserAddressAdmin)