from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.

def bag(request):
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id not in list(bag.keys()):
        bag[item_id] = 1

    # CODE NEEDED TO SEND MESSAGE TO USER - ITEM ALREADY IN BAG (As due to website context only 1 quantity can occur)
    request.session['bag'] = bag

    return redirect(redirect_url)

def remove_from_bag(request, item_id):

    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag.pop(item_id)

    # CODE NEEDED TO SEND MESSAGE TO USER - ITEM ALREADY IN BAG (As due to website context only 1 quantity can occur)
    request.session['bag'] = bag

    return HttpResponse(status=200)
