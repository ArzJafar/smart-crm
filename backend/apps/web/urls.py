from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Web URLs
    path('', views.main, name='main'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
    path('profile/', views.profile, name='profile'),

    # API URLs
    path('api/auth/', include([
        path('token/', obtain_auth_token, name='api_token'),
        path('login/', views.login_api, name='api_login'),
        path('logout/', views.logout_api, name='api_logout'),
        path('profile/', views.profile_api, name='api_profile'),
    ])),
]