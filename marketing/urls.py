from django.urls import path
from.import views


urlpatterns = [	
	path('robots/.txt',views.robots,name='robots'),

]