from django.urls import path
from.import views


urlpatterns=[
	# path('about/',views.about,name='about-page'),
	path('contact/',views.contact,name='contact-page'),
	path('privacy/',views.privacy,name='privacy-page'),
]