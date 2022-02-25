from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages


# Function that returns the current bag view
def bag(request):
    return render(request, 'bag/bag.html')


# Function that adds an item to the bag session
def add_to_bag(request, item_id):

    # Gets the pokemon details page the user came from
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    # Checks the item isnt in the bag
    if item_id not in list(bag.keys()):
        # Sets the pokemon as in the bag
        bag[item_id] = 1
        # Success message to notify user
        messages.success(request, 'Pokemon has been added to your bag.')

    # Updates the current bag session
    request.session['bag'] = bag
    return redirect(redirect_url)


# Function that removes an item from the bag
def remove_from_bag(request, item_id):

    # Gets the current bag session
    bag = request.session.get('bag', {})

    # Checks the pokemon is in the bag
    if item_id in list(bag.keys()):
        # Removes the pokemon from the bag
        bag.pop(item_id)
        # Success message to notify user
        messages.success(request, 'Pokemon has been removed to from bag.')

    # Updates the current bag session
    request.session['bag'] = bag

    return HttpResponse(status=200)
