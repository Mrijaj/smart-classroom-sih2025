from django.contrib import admin
from django.utils.html import format_html
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # 📋 Key columns for the admin list view
    list_display = ('student_name', 'subject_name', 'formatted_date', 'colored_status', 'created_at')

    # 🔍 Sidebar filters to isolate specific classes or dates
    list_filter = ('status', 'date', 'timetable_entry__subject', 'timetable_entry__classroom')

    # 🔎 Search across student details and subject names
    search_fields = (
        'student__username',
        'student__first_name',
        'student__last_name',
        'timetable_entry__subject__name'
    )

    # 📅 Chronological navigation at the top of the page
    date_hierarchy = 'date'

    # --- Prettier Column Logic ---

    def student_name(self, obj):
        """Displays Full Name if available, else Username"""
        if obj.student.first_name:
            return f"{obj.student.first_name} {obj.student.last_name}"
        return obj.student.username
    student_name.short_description = 'Student'
    student_name.admin_order_field = 'student__username'

    def subject_name(self, obj):
        """Accesses subject name via the timetable relation"""
        return obj.timetable_entry.subject.name
    subject_name.short_description = 'Subject'

    def formatted_date(self, obj):
        """Displays date in a clean format like '22 Feb, 2026'"""
        return obj.date.strftime("%d %b, %Y")
    formatted_date.short_description = 'Class Date'

    def colored_status(self, obj):
        """Renders a color-coded pill for status"""
        colors = {
            'present': '#198754',  # Success Green
            'absent': '#dc3545',   # Danger Red
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 600; text-transform: uppercase; font-size: 11px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.status
        )
    colored_status.short_description = 'Status'