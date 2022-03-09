from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages

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
    user_profile = None

    stripe_total = round(SUBSCRIPTION_COST*100)
    stripe.api_key = stripe_secret_key

    # Checks if there is a current user to avoid errors
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)
        user_profile = profile

        # Test to avoid crashing
        if profile:
            # Populates the form data with the user's
            form_data = {
                'full_name': profile.user,
                'email': profile.default_email,
                'user_trainer_code': profile.default_trainer_code,
            }

            # Checks if the user is subscribed
            subscription_status = profile.subscription
        else:
            messages.error(request, 'Cant find your profile, please relog.')
            return redirect(reverse('bag'))
        # Runs the complete order code if a form has been submitted, or if
        # the user is already subscribed
        if request.method == 'POST' or subscription_status:
            if not subscription_status:
                # Saves the user as subscribed if logged in and not subscribed
                messages.success(request,
                                 'You have now subscribed to our service.')
                profile = get_object_or_404(UserProfile, user=request.user)
                profile.subscription = True
                profile.save()

                messages.error(request, 'Check 4')

            order_form = OrderForm(form_data)

            # Checks the values in the user profile are valid
            if order_form.is_valid():
                bag = request.session.get('bag', {})
                order = order_form.save()
                # Adds each item to the order
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
                        messages.error(request,
                                       'There was an error with a pokemon')
                        return redirect(reverse('bag'))

                # Checkout is successful
                return redirect(reverse('checkout_success',
                                args=[order.order_number]))
            else:
                # One or more user detail is incorrect
                bag = request.session.get('bag', {})
                messages.error(request, 'There is an error with your details.')
                if not bag:
                    return redirect(reverse('products'))
            order_form = OrderForm()
    else:
        # Asks the user to log in before submitting
        messages.error(request, 'You must be logged in to submit requests.')
        return redirect(reverse('bag'))

    intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    # Sends context to checkout view for the script
    context = {
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'user_details': user_profile,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    # Checks user is logged in
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

    # Deletes the current bag session
    if 'bag' in request.session:
        del request.session['bag']

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
