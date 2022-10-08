from django.shortcuts import render
from django.http import HttpResponse
from .models import Gallery, Service, Slider, Staff, Testimonial, Blog
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    slider = Slider.objects.all()
    service = Service.objects.all()
    gallery = Gallery.objects.all()[:9]
    staff = Staff.objects.all()
    testimonies = Testimonial.objects.all()
    news = Blog.objects.all()

    context = {
        'sliders': slider,
        'services': service,
        'galleries': gallery,
        'staffs': staff,
        'testimonials': testimonies,
        'news': news,
    }
    return render(request, 'website/index.html', context)


def gallery(request):
    galleries = Gallery.objects.all()
    paginator = Paginator(galleries, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'page_obj': page_obj,
    }

    return render(request, 'website/gallery.html', context)