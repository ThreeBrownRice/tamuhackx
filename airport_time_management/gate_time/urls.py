# tsa_wait_time/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('get-gate/', views.get_gate, name='get_gate'),
    path('get-walk-time/',views.calculate_walk_time,name='calculate_walk_time')
]