from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import PGImage,PGInformation
from .forms import PGInformationForm,PGImageUploadForm

@login_required(login_url='login')
def home(request):
    return render(request,'home.html')


def display_details(request,area,rent):
   print(area,rent,type(area),type(rent))
   from django.db.models import Q
   rent=[int(x) for x in area.split('-')]
   if rent!=['0'] and area!='area':
        PI=PGInformation.objects.filter((Q(area=area)) & ((Q(fees2_eange=(rent[0],rent[1]))) | (Q(fees3_range=(rent[0],rent[1]))) | (Q(fees4_range=(rent[])))))
        rent=[int(i) for i in rent.split('-')]
        print(rent)
   
       
       
           
   return HttpResponse('hai')

def about_us(request):
    return render(request,'aboutus.html')
# MAX_IMAGE_SIZE = 1 * 1024 * 1024
def PGregister(request):
    if request.method == 'POST':
        form = PGInformationForm(request.POST, request.FILES)
        images=request.FILES.getlist('images')
        if form.is_valid() and images:
            pg_instance = form.save()
            images=request.FILES.getlist('images')
            for image in images:
                PGImage.objects.create(pg=pg_instance,image=image)
            return HttpResponse('Successfully uploaded')
        else:
            errors = []
            if not form.is_valid():
                errors.append('PG information is invalid.')

            if not image:
                errors.append('Image upload is invalid.')
                # You can also extend this to show form.errors and image_form.errors
            print(form.errors)
            print(image_form.errors)
            context = {
                'form': form,
                'image_form': image_form,
                'errors': errors,
            }
            return render(request, 'pgform.html', context)

    else:
        form = PGInformationForm()
        image_form = PGImageUploadForm()

    context = {
        'form': form,
        'image_form': image_form,
    }
    return render(request, 'pgform.html', context)

def pg_details(request,pk):
    pg=get_object_or_404(PGInformation,id=pk)
    return render(request,'pgdetails.html',{'pg':pg})
