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
   return HttpResponse('hai')

def about_us(request):
    return render(request,'aboutus.html')
# MAX_IMAGE_SIZE = 1 * 1024 * 1024
def PGregister(request):
    if request.method == 'POST':
        form = PGInformationForm(request.POST, request.FILES)


        print(form.is_valid(),'form')
        image_form = PGImageUploadForm(request.POST, request.FILES)
        print(request.FILES)
        print('request.files',request.FILES)
        print('hai',image_form.is_valid())

        if form.is_valid() and image_form.is_valid():
            print('bye')
            pg_instance = form.save()
            print('hey')
            images=request.Files.getlist('images')
            for image in images:
                PGImage.objects.create(pg=pg_instance,image=image)
            
            return HttpResponse('Successfully uploaded')
        else:
            errors = []
            if not form.is_valid():
                errors.append('PG information is invalid.')

            if not image_form.is_valid():
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
