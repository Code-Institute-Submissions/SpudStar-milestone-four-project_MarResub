from django.shortcuts import get_object_or_404
from goods.models import Info

# Currently used as the amount users have to pay to submit a request (£4.99)
SUBSCRIPTION_COST = 4.99


def bag_contents(request):

    bag_items = []
    product_count = 0

    # gets the users current session
    bag = request.session.get('bag', {})

    # Iterates through bag items to store them all in one variable
    for item_id, items in bag.items():
        product = get_object_or_404(Info, pk=item_id)
        product_count += 1
        bag_items.append({
            'item_id': item_id,
            'product': product,
        })

    # Stores the bag items and the total no of items in bag
    context = {
        'bag_items': bag_items,
        'product_count': product_count,
        }

    return context
