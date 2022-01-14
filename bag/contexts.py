from django.shortcuts import get_object_or_404
from goods.models import Info

SUBSCRIPTION_COST = 4.99

def bag_contents(request):

    bag_items = []
    product_count = 0
    
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Info, pk=item_id)
        product_count += 1
        bag_items.append({
            'item_id': item_id,
            'product': product,
        })

    context = {
        'bag_items': bag_items,
        'product_count': product_count,
        }

    return context
