# tsa_wait_time/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('get-shop/', views.get_shop, name='get_shop'),
    path('get-walk-time/',views.calculate_walk_time,name='calculate_walk_time')
]