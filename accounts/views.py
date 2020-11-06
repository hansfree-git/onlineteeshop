from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import Order,OrderItem
from django.urls import reverse
from django.http import Http404
from.models import UserAddress, UserDefaultAddress
from cart.cart import get_cart_items
from.forms import *
from django.urls import reverse

def register(request, template_name="registration/register.html"):
    """ view displaying customer registration form """
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = RegistrationForm(postdata)
        if form.is_valid():
            #form.save()
            user = form.save(commit=False)  # new
            user.email = postdata.get('email','')  # new
            user.save()  # new
            un = postdata.get('username','')
            pw = postdata.get('password1','')
            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:
                login(request, new_user)
                return redirect('my_account')

    else:
        form = RegistrationForm()
    page_title = 'User Registration'
    return render(request,template_name, locals())


@login_required
def my_account(request, template_name="registration/my_account.html"):
    """ page displaying customer account information, past order list and account options """
    page_title = 'My Account'
    try:
        orders = Order.objects.filter(user=request.user).order_by('-last_updated')
    except Order.DoesNotExist:
        pass
    name = request.user.username
    return render(request,template_name, locals())

def logged_out(request,template_name='registration/log_out.html'):
    logout(request)
    page_title = 'Logged Out'
    return render(request,template_name, locals())

def password_change_done(request,template_name='registration/password_change_done.html'):
    page_title = 'Password Change Done'
    return render(request,template_name, locals())


def order_info(request,template_name='registration/order_info.html'):
   form=UserAddressForm()
   user_addresses=UserAddress.objects.filter(user=request.user)
   billing_addresses=UserAddress.objects.get_billing_addresses(user=request.user)
   page_title = 'Order Info'
   return render(request,template_name, locals())


@login_required
def order_details(request, pk, template_name="registration/order_details.html"):
    """ displays the details of a past customer order; order details can only be loaded by the same 
    user to whom the order instance belongs.
    
    """
    order = get_object_or_404(Order, pk=pk, user=request.user)
    ordered=OrderItem.objects.filter(order=order)

    page_title = 'Order Details for Order #' + str(order.pk)
    return render(request,template_name, locals())


def add_address(request):
   if request.method=='POST':
      form=UserAddressForm(request.POST)
      if form.is_valid():
         new_address=form.save(commit=False)
         new_address.user=request.user
         phone=form.clean_phone
         new_address.save()
         """make address default by selecting the radio button"""
         is_default=form.cleaned_data['default']
         if is_default:
            default_address,created=UserDefaultAddress.objects.get_or_create(user=request.user)
            default_address.shipping_address=new_address
            default_address.billing_address=new_address
            default_address.save()
            messages.success(request,'Address has been successfully saved')
            return redirect('my_account')
   else:
      raise Http404('Form does not exist')


