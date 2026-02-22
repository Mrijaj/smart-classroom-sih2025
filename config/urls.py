"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


# Temporary home view (can remove later)
def home(request):
    return HttpResponse("Smart Classroom System is Running ✅")


urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', home, name='home'),

    # Accounts app (login/logout)
    path('accounts/', include('accounts.urls')),
]