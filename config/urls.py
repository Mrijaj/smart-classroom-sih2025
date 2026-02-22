from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Dashboard (Home Page)
    path('', include('dashboard.urls')),

    # Accounts (Login / Logout / Profile)
    path('accounts/', include('accounts.urls')),

    # Attendance module
    path('attendance/', include('attendance.urls')),

    # Timetable Management
    path('timetable/', include('timetable.urls')),

    # Activity Suggestion Engine
    path('activities/', include('activities.urls')),
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])