from django.utils import timezone
from .models import TimetableEntry
from activities.models import Activity, StudentGoal


def get_current_status(user):
    """
    Centralized DRY logic to determine current classroom status.
    Now includes Smart Activity Recommendations for free periods.
    """
    now = timezone.localtime(timezone.now())
    current_time = now.time()
    current_day = now.strftime('%a').lower()

    # 1. Query entries for the current time and day
    entries = TimetableEntry.objects.filter(
        day=current_day,
        timeslot__start_time__lte=current_time,
        timeslot__end_time__gte=current_time
    ).select_related('subject', 'classroom', 'timeslot')

    # 2. Identify Role
    role = getattr(user.userprofile, 'role', 'student')

    if role == 'student':
        ongoing_class = entries.filter(classroom__students=user).first()
    elif role == 'teacher':
        ongoing_class = entries.filter(teacher=user).first()
    else:
        ongoing_class = None

    # 3. Smart Logic: Personalized suggestions if in a Free Period
    suggested_activities = []
    if ongoing_class is None and role == 'student':
        # Fetch the student's goal profile
        goal = StudentGoal.objects.filter(student=user).first()
        if goal:
            # Recommend 3 tasks matching their primary interest
            suggested_activities = Activity.objects.filter(
                category=goal.primary_interest
            ).order_by('?')[:3]  # Randomize to keep it fresh

    return {
        'ongoing_class': ongoing_class,
        'is_free_period': ongoing_class is None,
        'current_time': current_time,
        'current_day': current_day.capitalize(),
        'role': role,
        'suggested_activities': suggested_activities,  # New Smart Data
    }