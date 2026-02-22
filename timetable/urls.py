from django.urls import path
from . import views

urlpatterns = [
    # ... your other paths
    path('view/', views.timetable_view, name='timetable_view'),
]