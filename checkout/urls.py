from django.urls import path
from.import views

urlpatterns = [
    path('show_checkout/', views.show_checkout, name='checkout'),
    path('receipt/<int:pk>', views.receipt, name='receipt'), #receives the pk of the order and provides the receipt
]