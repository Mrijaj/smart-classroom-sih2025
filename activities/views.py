from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Activity, ActivityLog


@login_required
def start_activity(request, activity_id):
    """
    API endpoint to log the start of an educational task.
    Triggered via AJAX from the dashboard.
    """
    if request.method == 'POST':
        activity = get_object_or_404(Activity, id=activity_id)

        # Create a new log entry for this student session
        log = ActivityLog.objects.create(
            student=request.user,
            activity=activity,
            start_time=timezone.now()
        )

        return JsonResponse({
            'status': 'success',
            'log_id': log.id,
            'message': f"Started tracking: {activity.title}"
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required
def complete_activity(request, log_id):
    """
    Marks a task as finished and calculates duration.
    """
    log = get_object_or_404(ActivityLog, id=log_id, student=request.user)

    if not log.completed:
        log.end_time = timezone.now()
        log.completed = True
        log.save()

        messages.success(request, f"Task '{log.activity.title}' completed! Time spent: {log.duration_minutes()} mins.")

    return redirect('dashboard')