from CLOTH import settings
from django.urls import path
from.import views

urlpatterns = [
    path('', views.show_cart, name='show-cart')
]
