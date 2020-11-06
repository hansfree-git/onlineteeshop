from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, OrderItem
from accounts.models import UserAddress
from accounts.forms import UserAddressForm
from django.conf import settings
from django.urls import reverse
from cart.models import CartItem
from cart.cart import *
from.utils import id_generator
import stripe




try:
    stripe_pub=settings.STRIPE_PUBLISHABLE_KEY
    stripe_key=settings.STRIPE_SECRET_KEY
except Exception as e:
    raise NotImplementedError(str(e))

stripe.api_key=stripe_key


def show_checkout(request, template_name='checkout/checkout.html'):
    try:
        stripe_pub=settings.STRIPE_PUBLISHABLE_KEY
        stripe_key=settings.STRIPE_SECRET_KEY
    except Exception as e:
        raise NotImplementedError(str(e))

    new_order=Order()
    if request.user.is_authenticated: 
        new_order.user=request.user
    else:
        new_order.user=None
    new_order.ip_address=request.META.get('REMOTE_ADDR')
    new_order.order_id=id_generator()
    new_order.save()

    if new_order.pk:
        """ if the order save succeeded """
        cart_items = get_cart_items(request)
        for ci in cart_items:
            """ create order item for each cart item """
            oi = OrderItem()
            oi.order = new_order
            oi.quantity = ci.quantity
            oi.price = ci.price  # now using @property
            oi.product = ci.product
            oi.save()
        
    final_amount=new_order.final_total
    
    try:    
        user_address=UserAddressForm()
        current_addresses=UserAddress.objects.filter(user=request.user)
        billing_addresses=UserAddress.objects.get_billing_addresses(user=request.user)
    except:
        user=None
        user_address=UserAddressForm()

    """retrieving the customer when he submits the payment form"""
    if request.method=='POST':
        try:
            user_stripe=request.user.userstripe.stripe_id
            customer=stripe.Customer.retrieve(user_stripe)
        except:
            customer=None
            pass
        """if customer actually exists we create a card for the customer
            with our already created stripe_id and 
            the token we obtain when he/she submits the payment form """
        if customer is not None:
            token=request.POST['stripeToken']
            """add the billing address and shipping to the customer, first getting the respective id's """
            billing_ad=request.POST['billing-address']
            shipping_ad=request.POST['shipping-address']

            try:
                billing_address_instance=UserAddress.objects.get(id=billing_ad)
            except:
                billing_ad=None
            try:
                shipping_address_instance=UserAddress.objects.get(id=shipping_ad)
            except:
                shipping_ad=None

            card=stripe.Customer.create_source( 
                user_stripe,
                source=token,
            )
            """ updating customer's card with shipping address"""
            card.address_city=billing_address_instance.shipping_city or None
            card.address_country=billing_address_instance.shipping_country or None
            card.address_line1=billing_address_instance.shipping_address_1 or None
            card.address_line2=billing_address_instance.shipping_address_2 or None
            card.address_state=billing_address_instance.shipping_state or None
            card.address_zip=billing_address_instance.shipping_zip or None
            card.name=billing_address_instance.user.username or None
            card.save()

            charge=stripe.Charge.create(
                  amount=int(final_amount * 100),
                  currency="usd",
                  source=card,
                  customer=customer,
                  description="Charge for %s" %{request.user.username}
                )

            # all set, clear the cart
            cart.empty_cart(request)

            if charge['captured']:

                new_order.status='SUBMITTED'
                new_order.transaction_id=id_generator(15)
                new_order.shipping_address= shipping_address_instance
                new_order.billing_address= billing_address_instance
                new_order.save()
                return redirect('receipt', pk=new_order.pk)

            if (charge['status']=='pending'):
                messages.warning('Processing your order.')
                return redirect('show-cart')
                
            if (charge['status']=='failed'):
               messages.error('There is a problem with your credit card.')
               return redirect('show-cart')

    page_title='Checkout'
    return render(request,template_name,locals())


def receipt(request,pk,template_name='checkout/receipt.html'):
    """ page displayed with order information after an order has been placed successfully """
    new_order=Order.objects.get(pk=pk)
    ordered=OrderItem.objects.filter(order=new_order)
    try:
        if new_order.status != 'SHIPPED' or new_order.status != 'CANCELLED':
            address_name=new_order.shipping_address.shipping_name
            address=new_order.shipping_address.shipping_address_1
            shipping_city=new_order.shipping_address.shipping_city
            shipping_state=new_order.shipping_address.shipping_state
            shipping_country=new_order.shipping_address.shipping_country
            shipping_zip=new_order.shipping_address.shipping_zip
            phone=new_order.shipping_address.phone
            transaction_id=new_order.transaction_id
        else:
            return redirect('show-cart')
    except:
        messages.warning(request,'Please complete your order and provide shipping address')

    page_title='Receipt'
    return render(request,template_name,locals())