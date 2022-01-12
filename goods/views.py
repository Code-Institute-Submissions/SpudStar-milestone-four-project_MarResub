from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Info

# Create your views here.

def all_products(request):

    products = Info.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category']
            queries = Q(type1__in=categories) | Q(type2__in=categories)
            products = products.filter(queries)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "No Pokemon name entered")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) 
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)