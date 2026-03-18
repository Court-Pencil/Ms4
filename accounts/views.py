from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})