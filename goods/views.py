from django.shortcuts import render, redirect, reverse, get_object_or_404
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
            queries = Q(type1=categories) | Q(type2=categories)
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


def product_detail(request, product_id):

    product = get_object_or_404(Info, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
