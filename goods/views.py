from django.shortcuts import render
from .models import Info

# Create your views here.

def all_products(request):

    data = Info.objects.all()

    context = {
        'products': data,
    }

    return render(request, 'products/products.html', context)