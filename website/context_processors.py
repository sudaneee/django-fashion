from pydoc import describe
from .models import Picture, GeneralInformation, ApplicationForms
from datetime import timedelta, date, datetime



def data_processor(request):
    logo = Picture.objects.get(tag='logo')
    small_logo = Picture.objects.get(tag='small-logo')
    profile = Picture.objects.get(tag='blank-profile')

    general_infomation = GeneralInformation.objects.filter().first()
    about_image = Picture.objects.get(tag='about-image')
    app_form = ApplicationForms.objects.get(description='tailoring-academy')


    return {
        'logo' : logo,
        'small_logo' : small_logo,
        'profile': profile,
        'general_infomation': general_infomation,
        'about_image': about_image,
        'date': datetime.today(),
        'form': app_form,
    }