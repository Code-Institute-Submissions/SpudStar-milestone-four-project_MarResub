from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Info, Category
from .forms import ProductForm
import math

# Filters products based on the either the pokemons type, or name


def all_products(request):

    # Sets up default values for declared variables
    products = Info.objects.all()
    category_name = None
    query = None
    categories = None
    page = 1
    # Sets constant for how many pokemon can appear on one page
    products_per_page = 20

    if request.GET:
        # Gets the pokemon type requested
        if 'category' in request.GET and 'category':
            categories = request.GET['category']
            # Checks both types for the type requested
            queries = Q(type1=categories) | Q(type2=categories)
            # Checks that the website knows the current category
            try:
                category_name = get_object_or_404(Category, pk=categories)
            except ValueError:
                category_name = None
            # Checks that the product list can be filtered
            try:
                products = products.filter(queries)
            except ValueError:
                products = Info.objects.all()

        # Checks if the search is by name
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                return redirect(reverse('products'))

            queries = Q(name__icontains=query)
            products = products.filter(queries)

        # Gets the page number requested
        if 'page_no' in request.GET:
            page = int(request.GET['page_no'])

    # Math to figure out how many pages are needed, and what entries are
    # displayed
    min_entry = (page-1)*products_per_page
    max_entry = page*products_per_page
    max_pages = math.ceil(len(products)/products_per_page)

    context = {
        'products': products,
        'search_term': query,
        'min_entry': min_entry,
        'max_entry': max_entry,
        'max_pages': max_pages,
        'category_name': category_name,
        'current_page': page,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):

    product = get_object_or_404(Info, pk=product_id)
    not_in_bag_check = True

    bag = request.session.get('bag', {})

    # Checks if the pokemon is already in the bag
    if str(product.id) in bag.keys():
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
            messages.success(request, 'Pokemon Added Successfully.')
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

    # Checks if the user wants to push the changes to a pokemon
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pokemon Edited Successfully.')
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
    messages.success(request, 'Pokemon Deleted Successfully.')
    return redirect(reverse('products'))
