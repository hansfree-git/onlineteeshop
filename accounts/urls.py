from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns=[
	path('ajax/add_address/', views.add_address, name='add-user-address'),
	path('register/',views.register,name='register'),
	path('accounts/my_account/',views.my_account,name='my_account'),
	path('accounts/logout/',views.logged_out,name='logout'),
	path('accounts/password_change/',auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html'),name='password_change'),
	path('accounts/password_change/done/',views.password_change_done),
	# order accounts
	path('order_info/',views.order_info,name='order_info'),
	path('order_details/<int:pk>/',views.order_details,name='order_details'),
]

# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']