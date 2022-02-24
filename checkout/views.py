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
    template = 'checkout/checkout.html'
    form_data = None

    stripe_total = round(SUBSCRIPTION_COST*100)
    stripe.api_key = stripe_secret_key

    intent = stripe.PaymentIntent.create(
                    amount=stripe_total,
                    currency=settings.STRIPE_CURRENCY,
                )

    # Code to check if user is subscribed already
    # Checks if there is a current user to avoid errors
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

        # Runs the complete order code if a form has been submitted, or if 
        # the user is already subscribed
        if request.method == 'POST' or subscription_status:

            if not subscription_status:
                # Saves the user as subscribed if logged in and not subscribed
                profile = get_object_or_404(UserProfile, user=request.user)
                profile.subscription = True
                profile.save()

            order_form = OrderForm(form_data)

            if order_form.is_valid():
                bag = request.session.get('bag', {})
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
    else:
        return redirect(reverse('view_bag'))

    context = {
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
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
