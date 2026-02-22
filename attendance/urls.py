from django.urls import path
from . import views

urlpatterns = [
    # 1. Teacher's Dashboard (Laptop/Projector)
    # Primary view for generating QR codes and monitoring class sessions.
    path('mark/', views.mark_attendance, name='mark_attendance'),

    # 2. Student's Scanning Endpoint (Mobile)
    # The secure token system for marking attendance via smartphone.
    path('scan/<str:token>/', views.student_scan_qr, name='student_scan_qr'),

    # 3. Live Feed API (Real-time Background Update)
    # Endpoint for AJAX polling to update the "Present Students" list.
    path('live-feed/<int:entry_id>/', views.get_live_attendance, name='get_live_attendance'),

    # 4. Student Analytics API (Dashboard Charts)
    # Feeds Chart.js on the student dashboard for personal attendance trends.
    path('analytics/', views.attendance_analytics, name='attendance_analytics'),

    # 5. Manual Attendance Endpoint (Battery Drain / Edge Cases)
    # Overrides the QR system for students with technical issues.
    path('manual-mark/<int:entry_id>/', views.manual_mark, name='manual_mark'),

    # 6. Admin Summary Dashboard (Engagement Analytics)
    # High-level overview of QR vs. Manual usage and peak system traffic.
    path('admin-summary/', views.admin_summary_dashboard, name='admin_summary'),
]