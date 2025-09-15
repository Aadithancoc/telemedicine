from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('symptom-checker/', views.symptom_checker, name='symptom_checker'),
    path('appointment/', views.appointment_scheduler, name='appointment_scheduler'),
    path('success/', views.success, name='success'),
]
