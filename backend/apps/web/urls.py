from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.main, name='main'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
    path('logout-pre/', views.logout_view, name='logout-pre'),
    path('profile/', views.profile, name='profile'),
    path('test-api/', views.test_api, name='test_api'),
]