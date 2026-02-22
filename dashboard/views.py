from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance.models import Attendance


@login_required
def dashboard_view(request):

    attendance_percentage = None

    if hasattr(request.user, 'userprofile'):
        if request.user.userprofile.role == 'student':
            attendance_percentage = Attendance.calculate_percentage(request.user)

    context = {
        'attendance_percentage': attendance_percentage
    }

    return render(request, 'dashboard/dashboard.html', context)