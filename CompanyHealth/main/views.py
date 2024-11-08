from django.shortcuts import render
from .models import *

def home(request):
    records = Records.objects.all()
    return render(request, 'main/index.html', {'records': records})
