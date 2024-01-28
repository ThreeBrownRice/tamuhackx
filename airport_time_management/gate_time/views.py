from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import random
from datetime import datetime
from gate_time.models import Gate

import googlemaps
import requests

def get_gate(request):
        shops = Gate.objects.all()
        # Serialize the data to JSON
        shop_list = []
        for shop in shops:
            shop_dict = {
                'name': shop.name,
                'latitude': shop.latitude,
                'longitude': shop.longitude,
            }
            shop_list.append(shop_dict)

        return JsonResponse({'gates': shop_list})

def getArrivalTime(gmaps, data, orig : dict,dest : dict, arrival_airport : datetime):
    '''Takes orig and dest as dictionaries and returns the duration in traffic in minutes'''
    #format of orig or dest needs to be {"lat": 30.6290011,"lng": -96.3588808}
    directions = gmaps.directions(orig, dest, arrival_time = arrival_airport)
     # Check if there's a valid result
    if data['rows'][0]['elements'][0]['status'] == 'OK':
        duration  = directions[0]['legs'][0]['duration']['value'] / 60
        return JsonResponse({'arrival_time': duration})
    else:
        return JsonResponse({'error': 'No valid route found'}, status=404)

def calculate_walk_time(request):
    google_api_key = "AIzaSyC5q8dkajhjuD6xFz5yncgymPsPmkKvyQk"
    #os.environ.get('')
    gmaps = googlemaps.Client(key=google_api_key)

    origin = request.GET.get('origin')  # Expected format: 'lat,lng'
    destination = request.GET.get('destination')  # Expected format: 'lat,lng'
    print(origin)
    print(destination)
    if not origin or not destination:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    response = requests.get(
        'https://maps.googleapis.com/maps/api/distancematrix/json',
        params={
            'origins': origin,
            'destinations': destination,
            'key': google_api_key
        }
    )

    if response.status_code == 200:
        data = response.json()
        return getArrivalTime(gmaps, data, origin, destination, datetime.now())
    else:
        return JsonResponse({'error': 'Failed to fetch data from Google Maps'}, status=response.status_code)
