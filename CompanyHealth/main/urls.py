from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('appointments/', views.appointments_view, name='appointments'),
    path('make_appointment/<int:doctor_id>/', views.make_appointment, name='make_appointment'),
    path('ourServices/', views.ourServices_view, name='ourServices'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('aboutUs/', views.aboutUs_view, name='aboutUs'),
    path('news/', views.news_view, name='news'),
    path('questions/', views.questions_view, name='questions'),
    path('editProfile/', views.editProfile_view, name='editProfile'),
    path('cancel_appointment/', views.cancel_appointment, name='cancel_appointment'),
    path('appointmentDoctor/<int:appointment_id>/', views.specific_appointment_for_patient, name='specific_appointment_for_patient'),
    path('appointmentPatient/<int:appointment_id>/', views.specific_appointment_for_doctor, name='specific_appointment_for_doctor'),
    path('home_visits_list/', views.home_visits_list, name='home_visits_list'),
    path('create_home_visit/', views.create_home_visit, name='create_home_visit'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('ask_question/', views.ask_question_view, name='ask_question'),
    path('get_available_slots/<int:doctor_id>/', views.get_available_slots, name='get_available_slots'),
]
