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
MAX_IMAGE_SIZE = 1 * 1024 * 1024
def PGregister(request):
    errors=[]
    if request.method=='POST':
        form=PGInformationForm(request.POST,request.FILES)
        image_form=PGImageUploadForm(request.POST,request.FILES)
        if form.is_valid() and image_form.is_valid():
            pg_instance=form.save()
            image_form.save(pg_instance=pg_instance)
            return HttpResponse('Successfully uploaded')
        else:
            if not form.is_valid():
                errors.append('pginformation is invalid')

            if not image_form.is_valid():
                reeor
            for img in images:
                if img.size > MAX_IMAGE_SIZE:
                    errors.append(f'image  Exceeds 1 MB size limite')
            if errors:
                return render(request,'pgform.html',context)

            # pg_instance=form.save()

            for image in images:
                context={'form': form, 'errors': errors}
                PGImage.objects.create(pg=pg_instance,image=image)
            return HttpResponse('successfully uploaded')
       
    else:
        form =PGInformationForm()
    context={'form':form}
    return render(request,'pgform.html',context)

def pg_details(request,pk):
    pg=get_object_or_404(PGInformation,id=pk)
    return render(request,'pgdetails.html',{'pg':pg})
