# tsa_wait_time/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('get-dt/', views.get_dt, name='get_dt'),
    
]