from django.db import models
from django.contrib.auth.models import User
from timetable.models import TimetableEntry


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )

    # Tracking the method of entry
    ENTRY_METHODS = (
        ('qr', 'QR Scan'),
        ('manual', 'Manual Entry'),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    timetable_entry = models.ForeignKey(
        TimetableEntry,
        on_delete=models.CASCADE,
        related_name='attendance_entries'
    )

    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    # Audit Trail: Who marked this and how?
    entry_method = models.CharField(
        max_length=10,
        choices=ENTRY_METHODS,
        default='qr'
    )

    marked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='manual_attendance_marks'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents duplicate attendance for the same student, same class, on the same day
        unique_together = ('student', 'timetable_entry', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.username} - {self.status} - {self.date}"

    @staticmethod
    def calculate_percentage(student):
        """Calculates the overall attendance percentage for a specific student."""
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(
            student=student,
            status='present'
        ).count()

        if total == 0:
            return 0

        return round((present / total) * 100, 2)