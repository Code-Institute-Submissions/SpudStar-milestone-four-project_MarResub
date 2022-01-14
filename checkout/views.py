from django.shortcuts import render, redirect, reverse

from .forms import OrderForm
# Create your views here.

def checkout(request):

    bag = request.session.get('bag', {})
    if not bag:
        return redirect(reverse('products'))

    order_form = OrderForm()
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51KHrw6AhGjWDCyMj1IR36w0iEB8YpJH7YMrPtB502Fu8Dt3FszbjxLfbv1CxyTUOSypv0RDlWKfn2xylyr8Pq7Hy00BgpF1aJk',
        'client_secret': 'secret',
        }

    return render(request, 'checkout/checkout.html', context)
