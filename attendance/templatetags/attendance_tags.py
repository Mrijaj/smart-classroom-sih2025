from django import template
from attendance.models import Attendance

register = template.Library()

@register.simple_tag
def get_user_attendance(user):
    return Attendance.calculate_percentage(user)