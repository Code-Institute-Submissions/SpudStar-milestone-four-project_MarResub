from django.shortcuts import render, redirect, reverse
from django.conf import settings

from bag.contexts import SUBSCRIPTION_COST
from .forms import OrderForm

import stripe
# Create your views here.

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    bag = request.session.get('bag', {})
    if not bag:
        return redirect(reverse('products'))

    order_form = OrderForm()

    stripe_total = round(SUBSCRIPTION_COST*100)
    stripe.api_key = stripe_secret_key

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY
    )
    
    print(intent)

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        }

    return render(request, 'checkout/checkout.html', context)
