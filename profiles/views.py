from django.shortcuts import render, get_object_or_404

from .models import UserProfile
from .forms import UserProfileForm


# Tries to retrieve the user's profile, and orders
def profile(request):
    # Checks if soeone not logged in is trying to access the profile app
    if not request.user.is_authenticated:
        return redirect(reverse('home'))

    profiles = get_object_or_404(UserProfile, user=request.user)

    # If the user updates their information, save it
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profiles)
        if form.is_valid():
            form.save()

    form = UserProfileForm(instance=profiles)
    orders = profiles.orders.all()

    context = {
        'form': form,
        'orders': orders,
        'subscription': profiles.subscription,
    }

    return render(request, 'profiles/profile.html', context)
