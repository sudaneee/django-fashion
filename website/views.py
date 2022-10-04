from django.shortcuts import render
from django.http import HttpResponse
from .models import Gallery, Service, Slider

# Create your views here.

def home(request):
    slider = Slider.objects.all()
    service = Service.objects.all()
    gallery = Gallery.objects.all()

    context = {
        'sliders': slider,
        'services': service,
        'galleries': gallery,
    }
    return render(request, 'website/index.html', context)
