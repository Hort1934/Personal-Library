from django.urls import path
from . import views


urlpatterns = [
    path("", views.main, name='main'),
    path("auth/", views.auth, name='home'),
    path("about/", views.about, name='about'),
    path("register/", views.register_form, name='register'),
    path("login/", views.login_form, name='login'),
    path("logout/", views.logout_request, name= "logout"),
    path('all/', views.all_users, name='all_users'),
    path('view/', views.view_user, name='view_user'),
    path('user_profile/', views.user_profile, name='user_profile'),
]