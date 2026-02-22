from django.contrib import admin
from .models import Activity, StudentGoal

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'estimated_time')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(StudentGoal)
class StudentGoalAdmin(admin.ModelAdmin):
    list_display = ('student', 'primary_interest', 'target_career')
    search_fields = ('student__username', 'target_career')