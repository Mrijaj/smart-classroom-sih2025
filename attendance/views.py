from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count  # Required for aggregation
from accounts.models import UserProfile
from timetable.models import TimetableEntry
from .models import Attendance
from .qr_utils import generate_classroom_qr, verify_qr_token
from datetime import timedelta


@login_required
def admin_summary_dashboard(request):
    """
    ADMIN VIEW: Summary analytics for SIH 2025 Demo.
    Shows QR vs Manual distribution and peak usage times.
    """
    profile = request.user.userprofile
    if profile.role != 'admin':
        messages.error(request, "Admin access required.")
        return redirect('dashboard')

    today = timezone.localdate()

    # 1. Breakdown of QR Scans vs Manual Entries
    method_stats = Attendance.objects.filter(date=today).values('entry_method').annotate(count=Count('id'))

    # 2. Peak Scan Hours (Hourly traffic distribution)
    # Note: 'strftime' usage may vary slightly between SQLite and PostgreSQL
    hourly_stats = Attendance.objects.filter(date=today).extra(
        select={'hour': "strftime('%%H', created_at)"}
    ).values('hour').annotate(count=Count('id')).order_by('hour')

    context = {
        'method_stats': method_stats,
        'hourly_stats': hourly_stats,
        'today': today,
    }
    return render(request, 'attendance/admin_summary.html', context)


@login_required
def mark_attendance(request):
    """ TEACHER VIEW (Laptop/Projector): Schedule and QR display. """
    profile = request.user.userprofile
    if profile.role not in ['teacher', 'admin']:
        messages.error(request, "Access denied. Teacher privileges required.")
        return redirect('dashboard')

    today = timezone.localdate()
    weekday_code = today.strftime('%a').lower()[:3]

    timetable_entries = TimetableEntry.objects.select_related(
        'classroom', 'subject', 'timeslot'
    ).filter(teacher=request.user, day=weekday_code)

    active_entry_id = request.GET.get('generate_for')
    qr_code_image = None
    selected_entry = None

    if active_entry_id:
        selected_entry = get_object_or_404(TimetableEntry, id=active_entry_id, teacher=request.user)
        qr_code_image = generate_classroom_qr(selected_entry.id)

    context = {
        'timetable_entries': timetable_entries,
        'today': today,
        'qr_code_image': qr_code_image,
        'selected_entry': selected_entry,
    }
    return render(request, 'attendance/mark_attendance.html', context)


@login_required
def manual_mark(request, entry_id):
    """ Allows teachers to mark students manually (e.g., dead battery). """
    profile = request.user.userprofile
    if profile.role not in ['teacher', 'admin']:
        messages.error(request, "Unauthorized.")
        return redirect('dashboard')

    entry = get_object_or_404(TimetableEntry, id=entry_id)
    students = entry.classroom.students.all().order_by('username')

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(User, id=student_id)

        Attendance.objects.update_or_create(
            student=student,
            timetable_entry=entry,
            date=timezone.localdate(),
            defaults={
                'status': 'present',
                'entry_method': 'manual',
                'marked_by': request.user
            }
        )

        messages.success(request, f"Manual attendance recorded for {student.username}.")
        # Redirect back to the marking page for that specific entry
        return redirect(f"/attendance/mark/?generate_for={entry_id}")

    return render(request, 'attendance/manual_mark.html', {'entry': entry, 'students': students})


@login_required
def student_scan_qr(request, token):
    """ Logic for scanning QR on mobile. """
    entry_id = verify_qr_token(token, max_age=60)
    if not entry_id:
        messages.error(request, "Invalid or expired QR code.")
        return redirect('dashboard')

    now = timezone.localtime(timezone.now()).time()
    entry = get_object_or_404(TimetableEntry, id=entry_id)

    # Enrollment and Timing checks
    if not (entry.timeslot.start_time <= now <= entry.timeslot.end_time):
        messages.error(request, f"Class '{entry.subject.name}' is not in session.")
        return redirect('dashboard')

    if not entry.classroom.students.filter(id=request.user.id).exists():
        messages.error(request, "Error: You are not enrolled in this classroom.")
        return redirect('dashboard')

    Attendance.objects.get_or_create(
        student=request.user,
        timetable_entry=entry,
        date=timezone.localdate(),
        defaults={'status': 'present', 'entry_method': 'qr'}
    )

    messages.success(request, "Successfully marked present!")
    return redirect('dashboard')


@login_required
def get_live_attendance(request, entry_id):
    """ API VIEW: Updates the teacher's projector feed in real-time. """
    entry = get_object_or_404(TimetableEntry, id=entry_id, teacher=request.user)
    attendance_list = Attendance.objects.filter(
        timetable_entry=entry, date=timezone.localdate()
    ).select_related('student').order_by('-created_at')

    data = [{
        'name': f"{a.student.first_name} {a.student.last_name}" if a.student.first_name else a.student.username,
        'time': timezone.localtime(a.created_at).strftime("%H:%M:%S"),
        'method': a.get_entry_method_display()
    } for a in attendance_list]

    return JsonResponse({'students': data})


@login_required
def attendance_analytics(request):
    """ JSON for student dashboard charts. """
    today = timezone.localdate()
    days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    labels = [day.strftime('%a') for day in days]
    counts = [Attendance.objects.filter(student=request.user, date=day, status='present').count() for day in days]

    return JsonResponse({'labels': labels, 'data': counts})