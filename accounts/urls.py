from django.urls import path
from . import views

urlpatterns = [
    # Authentication Routes
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Student Analytics & Performance Route
    path('profile/', views.profile_view, name='profile_view'),
]