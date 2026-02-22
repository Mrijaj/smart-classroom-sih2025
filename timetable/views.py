from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TimetableEntry


@login_required
def timetable_view(request):
    # Fetch all entries and group them by day for the template
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    timetable_data = {}

    for day in days:
        entries = TimetableEntry.objects.filter(day=day).select_related(
            'subject', 'classroom', 'timeslot', 'teacher'
        ).order_by('timeslot__start_time')

        if entries.exists():
            timetable_data[day.capitalize()] = entries

    return render(request, 'timetable/view_timetable.html', {'timetable_data': timetable_data})