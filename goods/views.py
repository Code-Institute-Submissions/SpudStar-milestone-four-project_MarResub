from django.shortcuts import render
from .models import Info

# Create your views here.

def all_products(request):

    products = Info.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)