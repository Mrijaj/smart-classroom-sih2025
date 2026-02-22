from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    """
    Stores individual tasks or educational content.
    Mapped to student interests for free period suggestions.
    """
    TAG_CHOICES = (
        ('dsa', 'Data Structures & Algorithms'),
        ('dev', 'Web Development'),
        ('apt', 'Aptitude & Logic'),
        ('soft', 'Soft Skills'),
        ('ast', 'Astronomy'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=TAG_CHOICES)
    external_link = models.URLField(blank=True, help_text="Link to YouTube, LeetCode, etc.")
    estimated_time = models.IntegerField(help_text="Time in minutes")

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

class StudentGoal(models.Model):
    """
    Links a student to their specific career path and interest.
    Used by the Suggestion Engine to filter relevant Activities.
    """
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='goal')
    primary_interest = models.CharField(
        max_length=20,
        choices=Activity.TAG_CHOICES,
        default='dsa'
    )
    target_career = models.CharField(
        max_length=100,
        help_text="e.g. System Analyst, Web Developer"
    )

    def __str__(self):
        return f"{self.student.username}'s Goals"

class ActivityLog(models.Model):
    """
    Tracks actual engagement.
    Allows teachers to verify student productivity during free periods.
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def duration_minutes(self):
        """Calculates total time spent on the task"""
        if self.end_time:
            diff = self.end_time - self.start_time
            return int(diff.total_seconds() / 60)
        return 0

    def __str__(self):
        return f"{self.student.username} started {self.activity.title}"