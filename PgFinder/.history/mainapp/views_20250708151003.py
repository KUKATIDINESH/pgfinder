from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import PGImage,PGInformation
from .forms import PGInformationForm,PGImageUploadForm

# @login_required(login_url='login')
def home(request):
    return render(request,'home.html')


def display_all_pg_details(request,area,rent):
    # print(area,rent,type(area),type(rent))
    from django.db.models import Q
    rent=[int(x) for x in rent.split('-')]
    # print(rent)
    if rent!=[0] and area!='area':

        PI=PGInformation.objects.filter((Q(area=area)) & ((Q(fees2__range=(rent[0],rent[1]))) | (Q(fees3__range=(rent[0],rent[1]))) | (Q(fees4__range=(rent[0],rent[1]))) | (Q(fees__range=(rent[0],rent[1]))) ))
    
    elif area=='area':
       PI=PGInformation.objects.filter(  (Q(fees2__range=(rent[0],rent[1]))) | (Q(fees3__range=(rent[0],rent[1]))) | (Q(fees4__range=(rent[0],rent[1]))) | (Q(fees__range=(rent[0],rent[1])))  )  
        
    else:
       PI=PGInformation.objects.filter(area=area)
    #    print(PI)
    
    context={'PI':PI}
    return render(request,'display_all_pg_details.html',context)

def about_us(request):
    return render(request,'aboutus.html')
# MAX_IMAGE_SIZE = 1 * 1024 * 1024
@login_required(login_url='login')
def PGregister(request):
    form = PGInformationForm()
    image_form = PGImageUploadForm()

    context = {
        'form': form,
        'image_form': image_form,
    }
    if request.method == 'POST':
        form = PGInformationForm(request.POST, request.FILES)
        images=request.FILES.getlist('images')
       
        if form.is_valid() and images:
            pg_instance1=form.save(commit=False)
            pg_instance1.pguser=request.user
            
            pg_instance1.save()
           
            for image in images:
                PGImage.objects.create(pg=pg_instance1,image=image)
            return HttpResponse('Successfully uploaded')
        else:
            errors = []
            if not form.is_valid():
                errors.append('PG information is invalid.')

            if not images:
                errors.append('Image upload is invalid.')
                # You can also extend this to show form.errors and image_form.errors
            # print(form.errors)
            # print('hai')
            # print(image_form.errors)
            context = {
                'form': form,
                'image_form': image_form,
                'errors': errors,
            }
            return render(request, 'pgform.html', context)
    return render(request, 'pgform.html', context)
@login_required(login_url='login')
def pg_modify(request,pk):
    context={}
    try:
        pg=PGInformation.objects.get(id=pk)
    except:
        return HttpResponse("PG not found")
    if request.method=='POST':
        form=PGInformationForm(request.POST,request.FILES,instance=pg)
        if form.is_valid():
            form.save()
            new_images=request.FILES.getlist('images')
            if new_images:
                PGImage.objects.filter(pg=pg).delete()
                for image in new_images:
                    PGImage.objects.create(pg=pg,image=image)
                for image in images:
                PGImage.objects.create(pg=pg_instance1,image=image)
            return redirect('home')
        else:
            return HttpResponse('something went wrong..')



    form=PGInformationForm(instance=pg)
    image_form=PGImageUploadForm()
    context={
        'form':form,
        'image_form':image_form,
        'images':pg.images.all()
    }
    return render(request,'pgmodify.html',context)

def pg_details(request,pk):
    try:
        pg=get_object_or_404(PGInformation,id=pk)
    except:
        return HttpResponse('Pg details not found')
    return render(request,'pgdetails.html',{'pg':pg})
@login_required(login_url='login')
def pglist_for_modify(request):
    try:
        pgs=PGInformation.objects.filter(pguser=request.user)
        if not pgs:
             return HttpResponse('no pg foung with is user ok')
    except:
        return HttpResponse('no pg foung with is user')
    context={
        'pgs':pgs
    }
    return render(request,'pglist_for_modification.html',context)
@login_required(login_url='login')
def pg_delete(request,pk):
    try:
        pg=PGInformation.objects.get(id=pk)
        pg.delete()
        
    except:
        return HttpResponse("PG not found")
    return redirect('pglist_for_modification')