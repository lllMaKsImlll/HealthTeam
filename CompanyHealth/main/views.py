from django.shortcuts import render
from .models import *

def home(request):
    doctors = Doctor.objects.all()
    return render(request, 'main/index.html', {'doctors': doctors})
