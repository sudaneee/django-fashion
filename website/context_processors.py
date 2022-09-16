from .models import Picture 



def data_processor(request):
    logo = Picture.objects.get(tag='logo')
    small_logo = Picture.objects.get(tag='small-logo')
    profile = Picture.objects.get(tag='blank-profile')


    return {
        'logo' : logo,
        'small_logo' : small_logo,
        'profile': profile,
    }