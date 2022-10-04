from django.shortcuts import render
from django.http import HttpResponse
from .models import Gallery, Service, Slider, Staff

# Create your views here.

def home(request):
    slider = Slider.objects.all()
    service = Service.objects.all()
    gallery = Gallery.objects.all()
    staff = Staff.objects.all()

    context = {
        'sliders': slider,
        'services': service,
        'galleries': gallery,
        'staffs': staff,
    }
    return render(request, 'website/index.html', context)
