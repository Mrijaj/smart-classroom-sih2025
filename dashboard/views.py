from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance.models import Attendance
from timetable.services import get_current_status

@login_required
def dashboard_view(request):
    # 1. Get the centralized status (Ongoing class vs Free period)
    context = get_current_status(request.user)

    # 2. Add role-specific data (Attendance for students)
    if context['role'] == 'student':
        context['attendance_percentage'] = Attendance.calculate_percentage(request.user)
    else:
        context['attendance_percentage'] = None

    return render(request, 'dashboard/dashboard.html', context)