from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import UserProfile
from activities.models import ActivityLog
from attendance.models import Attendance


def user_login(request):
    """Handles secure login and triggers the welcome popup."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                profile = UserProfile.objects.filter(user=user).first()
                role_name = profile.role.title() if profile else "User"

                messages.success(
                    request,
                    f"Welcome back, {user.first_name or username}! You are logged in as {role_name}.",
                    extra_tags='login_success'
                )
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login details.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile_view(request):
    """
    Aggregates student performance data for the Profile Page.
    """
    user = request.user

    # 1. Calculate total minutes from completed activity logs
    total_minutes = ActivityLog.objects.filter(
        student=user,
        completed=True
    ).aggregate(Sum('activity__estimated_time'))['activity__estimated_time__sum'] or 0

    # 2. Count total attendance records marked as present
    total_attended = Attendance.objects.filter(
        student=user,
        status='present'
    ).count()

    # 3. Fetch all activity logs to display the history table
    logs = ActivityLog.objects.filter(student=user).select_related('activity').order_by('-start_time')

    context = {
        'total_minutes': total_minutes,
        'total_attended': total_attended,
        'logs': logs,
    }
    return render(request, 'accounts/profile.html', context)


def user_logout(request):
    """Handles session termination and redirects to login."""
    logout(request)
    messages.info(request, "Logged out successfully. See you soon!")
    return redirect('login')