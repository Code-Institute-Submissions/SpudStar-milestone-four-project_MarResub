from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings

from goods.models import Info
from profiles.models import UserProfile
from .models import Order, OrderLineItem

# Gets the cost of a request
from bag.contexts import SUBSCRIPTION_COST
from .forms import OrderForm
from profiles.forms import UserProfileForm

import stripe

# Uses the stripe keys and the form data to make a purchase


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    subscription_status = False
    client_secret_value = None
    template = 'checkout/checkout.html'
    bag = request.session.get('bag', {})

    # Checks if there is a current user
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)
        if profile:
            # Populates the form data with the user's
            form_data = {
                'full_name': profile.user,
                'email': profile.default_email,
                'user_trainer_code': profile.default_trainer_code,
            }
            # Checks if the user is subscribed
            subscription_status = profile.subscription

    # Checks if the person needs to pay anything
    if not subscription_status:

        if request.method == 'POST':

            # If it is a guest user, saves the form data
            if not request.user.is_authenticated:
                form_data = {
                    'full_name': request.POST['full_name'],
                    'email': request.POST['email'],
                    'user_trainer_code': request.POST['user_trainer_code'],
                }

            # Creates the intent to pay the subscription

            stripe_total = round(SUBSCRIPTION_COST*100)
            stripe.api_key = stripe_secret_key

            intent = stripe.PaymentIntent.create(
                    amount=stripe_total,
                    currency=settings.STRIPE_CURRENCY,
                )
            client_secret_value = intent.client_secret

            # Saves the user as subscribed if logged in
            if request.user.is_authenticated:
                profile = get_object_or_404(UserProfile, user=request.user)
                profile.subscription = True
                profile.save()

    order_form = OrderForm(form_data)
    
    if subscription_status or request.method == 'POST':
        # If the form is valid, creates an order
        
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in bag.items():
                try:
                    product = Info.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                        )
                    order_line_item.save()
                # If a pokemon somehow doesn't exist, returns to bag
                except Info.DoesNotExist:
                    order.delete()
                    return redirect(reverse('view_bag'))

                return redirect(reverse('checkout_success',
                                args=[order.order_number]))
        else:
            bag = request.session.get('bag', {})
            if not bag:
                return redirect(reverse('products'))

        order_form = OrderForm()

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret_value,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        profile_data = {
            'default_trainer_number': order.user_trainer_code,
            'default_email': order.email,
        }

        user_profile_form = UserProfileForm(profile_data, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()

    if 'bag' in request.session:
        del request.session['bag']

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
