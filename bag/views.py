from django.shortcuts import render, redirect, reverse, HttpResponse
# Logic similar to Boutique Ado, no much to change


# Function that returns the current bag view
def bag(request):
    return render(request, 'bag/bag.html')


# Function that adds an item to the bag session
def add_to_bag(request, item_id):

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id not in list(bag.keys()):
        bag[item_id] = 1

    request.session['bag'] = bag

    return redirect(redirect_url)


# Function that removes an item from the bag
def remove_from_bag(request, item_id):

    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag.pop(item_id)

    request.session['bag'] = bag

    return HttpResponse(status=200)
