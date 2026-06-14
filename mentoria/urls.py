from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Onboarding
    path('interests/', views.interests_view, name='interests'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('lessons/<uuid:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<uuid:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
    
    # Opportunities
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('opportunities/<slug:slug>/', views.opportunity_detail, name='opportunity_detail'),
    path('opportunities/<uuid:opportunity_id>/save/', views.save_opportunity, name='save_opportunity'),
    
    # News
    path('news/', views.news_list, name='news_list'),
    path('news/<uuid:slug>/', views.news_detail, name='news_detail'),
]
