from django.shortcuts import render, redirect
from django.contrib import messages
from .import forms, cart


def show_cart(request, template_name="cart/cart.html"):
    """ view function for the page displaying the customer shopping cart, and allows for the updating of quantities
    and removal product instances 

    """
    if request.method == 'POST':
        postdata = request.POST.copy()
        try:
            if postdata['submit'] == 'Remove':
                cart.remove_from_cart(request)
            if postdata['submit'] == 'Update':
                cart.update_cart(request)
        except ValueError:
            message=messages.error(request,"Oops!  That was no valid number.Try only integer...")
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)

    return render(request, template_name, locals())
