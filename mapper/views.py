from django.shortcuts import render
from django.http import HttpResponse
import os

GOOGLE_MAPS_API_KEY = os.environ.get('MAPS_KEY')

def index(request):
    return render(request, 'mapper/index.html', {'MAPS_KEY': GOOGLE_MAPS_API_KEY})
