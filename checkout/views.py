from django.shortcuts import render, redirect, reverse

from .forms import OrderForm
# Create your views here.

def checkout(request):

    bag = request.session.get('bag', {})
    if not bag:
        return redirect(reverse('products'))

    order_form = OrderForm()
    context = {'order_form': order_form}

    return render(request, 'checkout/checkout.html', context)
