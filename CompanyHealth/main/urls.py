from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('appointments/', views.appointments_view, name='appointments'),
    path('ourServices/', views.ourServices_view, name='ourServices'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('aboutUs/', views.aboutUs_view, name='aboutUs'),
    path('news/', views.news_view, name='news'),
    path('questions/', views.questions_view, name='questions'),
    path('editProfile/', views.editProfile_view, name='editProfile'),
]
