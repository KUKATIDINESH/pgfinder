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
   
    from django.db.models import Q
    rent=[int(x) for x in rent.split('-')]
    
    if rent != [0] and area != 'area':

        PI=PGInformation.objects.filter((Q(area=area)) & ((Q(fees2__range=(rent[0],rent[1]))) | (Q(fees3__range=(rent[0],rent[1]))) | (Q(fees4__range=(rent[0],rent[1]))) | (Q(fees__range=(rent[0],rent[1]))) ))
    
    elif area=='area':
       PI=PGInformation.objects.filter(  (Q(fees2__range=(rent[0],rent[1]))) | (Q(fees3__range=(rent[0],rent[1]))) | (Q(fees4__range=(rent[0],rent[1]))) | (Q(fees__range=(rent[0],rent[1])))  )  
        
    else:
       PI=PGInformation.objects.filter(area=area)
    
    
    context={'PI':PI}
    return render(request,'display_all_pg_details.html',context)

def about_us(request):
    return render(request,'aboutus.html')

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
            
            # Show success message and redirect to home
            from django.contrib import messages
            messages.success(request, 'PG registered successfully! Your listing is now live.')
            return redirect('home')
        else:
            errors = []
            if not form.is_valid():
                errors.append('PG information is invalid.')

            if not images:
                errors.append('Image upload is invalid. Upload proper image.')
 
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
        # Check if user owns this PG
        if pg.pguser != request.user:
            return HttpResponse("You don't have permission to modify this PG")
    except:
        return HttpResponse("PG not found")
    
    if request.method=='POST':
        form=PGInformationForm(request.POST,request.FILES,instance=pg)
        if form.is_valid():
            # Handle sharing types - if unchecked, set to False and clear related fields
            if 'two_sharing' not in request.POST:
                pg.two_sharing = False
                pg.vacancy2 = None
                pg.fees2 = None
            if 'three_sharing' not in request.POST:
                pg.three_sharing = False
                pg.vacancy3 = None
                pg.fees3 = None
            if 'four_sharing' not in request.POST:
                pg.four_sharing = False
                pg.vacancy4 = None
                pg.fees4 = None
            if 'other_sharing' not in request.POST:
                pg.other_sharing = False
                pg.vacancy = None
                pg.fees = None
            
            # Handle facilities - if unchecked, set to False
            if 'washing_machine' not in request.POST:
                pg.washing_machine = False
            if 'water_heater' not in request.POST:
                pg.water_heater = False
            if 'ac' not in request.POST:
                pg.ac = False
                
            form.save()
            
            # Handle image uploads
            new_images=request.FILES.getlist('images')
            if new_images:
                for image in new_images:
                    PGImage.objects.create(pg=pg,image=image)
            
            # Show success message
            from django.contrib import messages
            messages.success(request, 'PG updated successfully!')
            return redirect('pglist_for_modification')
        else:
            # If form is invalid, show errors
            context = {
                'form': form,
                'image_form': PGImageUploadForm(),
                'images': pg.images.all(),
                'pg': pg,
                'errors': [str(error) for error in form.errors.values()]
            }
            return render(request,'pgmodify.html',context)

    form=PGInformationForm(instance=pg)
    image_form=PGImageUploadForm()
    context={
        'form':form,
        'image_form':image_form,
        'images':pg.images.all(),
        'pg':pg
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
             return HttpResponse('no pg found with this user')
    except:
        return HttpResponse('no pg found with this user')
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

@login_required(login_url='login')
def delete_image(request, image_id):
    try:
        image = get_object_or_404(PGImage, id=image_id)
        # Check if the user owns the PG associated with this image
        if image.pg.pguser == request.user:
            image.delete()
            return redirect('modifypg', pk=image.pg.id)
        else:
            return HttpResponse("You don't have permission to delete this image")
    except:
        return HttpResponse("Image not found")