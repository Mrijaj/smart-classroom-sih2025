from django.db import models
from django.contrib.auth.models import User


class ClassRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # Connect students to classroom
    students = models.ManyToManyField(
        User,
        related_name='classrooms',
        blank=True
    )

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class TimetableEntry(models.Model):

    DAY_CHOICES = (
        ('sun', 'Sunday'),
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
    )

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name='timetable_entries'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teaching_entries'
    )

    timeslot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE
    )

    day = models.CharField(
        max_length=3,
        choices=DAY_CHOICES
    )

    class Meta:
        unique_together = ('classroom', 'timeslot', 'day')
        ordering = ['day', 'timeslot']

    def __str__(self):
        return f"{self.classroom} - {self.subject} ({self.get_day_display()})"