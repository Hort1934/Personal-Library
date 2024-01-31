from django.urls import path
from . import views


urlpatterns = [
    path("", views.main, name='main'),
    path("auth/", views.auth, name='home'),
    path("about/", views.about, name='about'),
    path("register/", views.register_form, name='register'),
    path("login/", views.login_form, name='login'),
    # path("un_login/", views.un_login_form, name='un_login'),
    path("logout/", views.logout_request, name= "logout"),
    path('all/', views.all_users, name='all_users'),
    path('view/', views.view_user, name='view_user'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('submit_question/', views.submit_question, name='submit_question'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('analytics/', views.user_role_distribution, name='analytics'),
    path('analytics_2/', views.user_registration_by_year, name='analytics_2'),
    path('analytics_3/', views.user_registration_by_day, name='analytics_3'),
    path('analytics_dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
    path('edit_profile/', views.user_profile, name='edit_profile'),

]