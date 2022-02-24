from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Info
from .forms import ProductForm
import math


# Filters products based on the either the pokemons type, or name

def all_products(request):

    products = Info.objects.all()
    query = None
    categories = None
    page = 1
    products_per_page = 20

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category']
            # Checks both types for the type requested
            queries = Q(type1=categories) | Q(type2=categories)
            try:
                products = products.filter(queries)
            except:
                products = Info.objects.all()

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) 
            products = products.filter(queries)

        if 'page_no' in request.GET:
            page = int(request.GET['page_no'])

    min_entry = (page-1)*products_per_page
    max_entry = page*products_per_page
    max_pages = math.ceil(len(products)/products_per_page)

    context = {
        'products': products,
        'search_term': query,
        'min_entry': min_entry,
        'max_entry': max_entry,
        'max_pages': max_pages,
        'category_no': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):

    product = get_object_or_404(Info, pk=product_id)
    not_in_bag_check = True

    bag = request.session.get('bag', {})

    if product.id not in list(bag.keys()):
        bag[item_id] = 1
        not_in_bag_check = False

    context = {
        'product': product,
        'not_in_bag': not_in_bag_check,
    }

    return render(request, 'products/product_detail.html', context)


# Allows pokemon to be added
def add_product(request):

    # Stops the user accessing via url
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        # Checks to see if the pokemon info is valid
        if form.is_valid():
            form.save()
            return redirect(reverse('add_product'))
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


# Allows an existing pokemon to be edited
def edit_product(request, product_id):

    # Stops the user accessing via url
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    product = get_object_or_404(Info, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('product_detail', args=[product.id]))
    else:
        form = ProductForm(instance=product)

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)


# Allows a pokemon to be removed from the database
def delete_product(request, product_id):

    # Stops the user accessing via url
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    product = get_object_or_404(Info, pk=product_id)
    product.delete()
    return redirect(reverse('products'))
