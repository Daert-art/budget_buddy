from django.urls import path
from django.contrib.auth import views as auth_views

from apps.users import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('users/', views.RegisterView.as_view(), name='users'),
]