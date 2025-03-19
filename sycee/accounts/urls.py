# accounts/urls.py
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('login/', views.login_view, name='login'),
# ]

urlpatterns = [
    path('login/', include('django.contrib.auth.urls')),  # Includes login, logout, etc.
]