from .models import Picture, GeneralInformation



def data_processor(request):
    logo = Picture.objects.get(tag='logo')
    small_logo = Picture.objects.get(tag='small-logo')
    profile = Picture.objects.get(tag='blank-profile')

    general_infomation = GeneralInformation.objects.filter().first()
    about_image = Picture.objects.get(tag='about-image')


    return {
        'logo' : logo,
        'small_logo' : small_logo,
        'profile': profile,
        'general_infomation': general_infomation,
        'about_image': about_image,
    }