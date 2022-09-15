from .models import Picture 



def data_processor(request):
    logo = Picture.objects.get(tag='logo')
    profile = Picture.objects.get(tag='blank-profile')


    return {
        'logo' : logo,
        'profile': profile,
    }