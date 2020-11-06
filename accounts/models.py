from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class UserStripe(models.Model):
	user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	stripe_id=models.CharField(max_length=120)

	def __str__(self):
		return self.stripe_id


def get_or_create_stripe(sender,user,*args,**kwargs):
	try:
		""" gets user's stripe id from the model """
		user.userstripe.stripe_id

		""" sets a new one if it doesn't exist """
	except UserStripe.DoesNotExist	:

		customer=stripe.Customer.create(
			name=user.username, 
			#email=user.email 
		)
		new_user_stripe=UserStripe.objects.create(
			#the customer json response is where we got the id
			user=user,
			stripe_id=customer.id
		)
	except:
		pass

user_logged_in.connect(get_or_create_stripe)

""" make customers default address"""

class UserDefaultAddress(models.Model):
	user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
	shipping_address=models.ForeignKey("UserAddress",
		null=True,on_delete=models.CASCADE, related_name='user_default_shipping_address')
	billing_address=models.ForeignKey("UserAddress",
		null=True,on_delete=models.CASCADE, related_name='user_default_billing_address')

	def __str__(self):
		return self.user.username



class UserAddressManager(models.Manager):
	def get_billing_addresses(self, user):
		return super(UserAddressManager,self).filter(billing=True).filter(user=user)


class UserAddress(models.Model):
	user=models.ForeignKey(User,null=True, on_delete=models.CASCADE)
	shipping_name = models.CharField(max_length=120)
	shipping_address_1 = models.CharField(max_length=120)
	shipping_address_2 = models.CharField(max_length=120, blank=True)
	shipping_city = models.CharField(max_length=120)
	shipping_state = models.CharField(max_length=120)
	shipping_country = models.CharField(max_length=120)
	shipping_zip = models.CharField(max_length=10)
	phone = models.CharField(max_length=20)
	shipping=models.BooleanField(default=True)
	billing=models.BooleanField(default=False)
	timestamp=models.DateTimeField(auto_now_add=True,auto_now=False)
	updated=models.DateTimeField(auto_now_add=False,auto_now=True)

	def __str__(self):
		return self.get_address()

	class Meta:
		ordering=['-updated','-timestamp']	

		"""return a short address from the database """
	def get_address(self):
		return "%s,%s,%s,%s,%s" %(self.shipping_name,
			self.shipping_address_1,
			self.shipping_city,
			self.shipping_state,
			self.shipping_country,
			)

	objects=UserAddressManager()



# from checkout.models import BaseOrderInfo

# class UserProfile(BaseOrderInfo):
#     """ stores customer order information used with the last order placed; can be attached to the checkout order form
#     as a convenience to registered customers who have placed an order in the past.
    
#     """
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')
    
#     def __str__(self):
#         return 'User Profile for: ' + self.user.username