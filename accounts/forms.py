from django import forms
from .models import UserAddress
from django.contrib.auth.forms import UserCreationForm
import re
from re import sub

class UserAddressForm(forms.ModelForm):
	default=forms.BooleanField(label='Make Default')
	class Meta:
		model=UserAddress
		fields=[	
			"shipping_name" ,
			"shipping_address_1" ,
			"shipping_address_2", 
			"shipping_city" ,
			"shipping_state" ,
			"shipping_country" ,
			"shipping_zip",
			"phone",
		]
	""" gets rid of all non-number characters """

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		stripped_phone=phone.strip()
		if len(stripped_phone)<10:
			raise forms.ValidationError('Enter a valid phone number with area code. (e.g. 555-555-5555)')
		return self.cleaned_data['phone']

        
class RegistrationForm(UserCreationForm):
    """ subclass of Django's UserCreationForm, to handle customer registration with a required minimum length
    and password strength. Also contains an additional field for capturing the email on registration.
    
    """
    password1 = forms.RegexField(label="Password", regex=r'^(?=.*\W+).*$', 
                                 help_text='Password must be six characters long and contain at least one non-alphanumeric character.',
                                 widget=forms.PasswordInput, min_length=6)
    password2 = forms.RegexField(label="Password confirmation", regex=r'^(?=.*\W+).*$',
                                 widget=forms.PasswordInput, min_length=6)
    email = forms.EmailField(max_length="50")