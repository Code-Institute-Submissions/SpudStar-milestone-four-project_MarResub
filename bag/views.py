from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

# Function that returns the current bag view


def bag(request):
    return render(request, 'bag/bag.html')


# Function that adds an item to the bag session
def add_to_bag(request, item_id):

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    # Checks the item isnt in the bag
    if item_id not in list(bag.keys()):
        bag[item_id] = 1
        messages.success(request, 'Pokemon has been added to your bag.')

    request.session['bag'] = bag
    return redirect(redirect_url)


# Function that removes an item from the bag
def remove_from_bag(request, item_id):

    bag = request.session.get('bag', {})

    # Checks the item is in the bag
    if item_id in list(bag.keys()):
        bag.pop(item_id)
        messages.success(request, 'Pokemon has been removed to from bag.')

    request.session['bag'] = bag

    return HttpResponse(status=200)
