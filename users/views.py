from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

from django.core.exceptions import ObjectDoesNotExist
from applications.models import Period, Application
import datetime

# Create your views here.


def home(request):
    """
    View redirects users according to their authentication status
    """
    try:
        current_period = Period.objects.get(
            year=datetime.date.today().year)
    except ObjectDoesNotExist:
        current_period = None

    context = {
        'title': 'Home',
        'current_period': current_period
    }
    if request.user.is_anonymous:
        return render(request, 'users/dashboard/anonymous.html', context)
    else:
        if request.user.user_type in [0, 1]:
            total_applications = Application.objects.filter(
                period=current_period).count()
            recommended_applications = Application.objects.filter(
                period=current_period, recommended=True).count()

            context['total_applications'] = total_applications
            context['recommended_applications'] = recommended_applications

            return render(request, 'users/dashboard/staff.html', context)
        elif request.user.user_type == 2:
            return render(request, 'users/dashboard/applicant.html', context)


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully')
        return redirect(request.META['HTTP_REFERER'])

    context = {
        'title': 'Profile',
        'form': form
    }

    return render(request, 'users/profile.html', context)
