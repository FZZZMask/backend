from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health),
    path('pm25/', views.pm25),
    path('cold/', views.cold),
]
