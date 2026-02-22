from django.urls import path
from .views import dashboard_view

urlpatterns = [
    # Main landing page after login
    path('', dashboard_view, name='dashboard'),
]