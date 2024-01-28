from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import random
from datetime import datetime
import requests
from dateutil import parser
import pytz
# from gate_time.models import Gate

def get_dt(request):
    years,month,day = request.GET.get('day').split('-') #expected format - YYYY-MM-DD
    flight_number = request.GET.get('flightNum')
    c_year, c_month, c_day = request.GET.get('current_day').split('-')
    c_hours, c_min = request.GET.get('current_time').split('-')
    # years = dep_day.year
    # month = dep_day.month
    # day = dep_day.day

    URL = f'https://american-airlines-data-6d1bb5ff9b3a.herokuapp.com/flights?date={years}-{month}-{day}&flightNumber={flight_number}'
    # edit_url = f'flights?date={years}-{month}-{day}&flightNumber={flight_number}'
    data = requests.get(URL).json()
    timestamp_str = data[0]['departureTime']
    dt = parser.parse(timestamp_str)
    timezone_str = data[0]['origin']['timezone']
    timezone_info = pytz.timezone(timezone_str)
    c_dt = datetime(int(c_year), int(c_month), int(c_day), int(c_hours), int(c_min))
    # Add timezone information to the datetime object
    c_dt = timezone_info.localize(c_dt)
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    min = dt.minute
    
    diff_dt = (dt - c_dt).total_seconds() / 60
    return JsonResponse({'departure-time': {'dep_time' : dt, 'year' : year, 'month' : month, 'day' : day, 'hour' : hour, 'minute' : min}, 'difference_min' : diff_dt})