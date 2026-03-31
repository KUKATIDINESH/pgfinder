from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from datetime import date
# Create your views here.
from .models import PGImage,PGInformation,Booking,BookingReview
from .forms import PGInformationForm,PGImageUploadForm,BookingForm,BookingReviewForm,BookingCancellationForm


SHARING_FIELD_MAP = {
    'single': ('other_sharing', 'vacancy', 'fees'),
    'double': ('two_sharing', 'vacancy2', 'fees2'),
    'triple': ('three_sharing', 'vacancy3', 'fees3'),
    'four': ('four_sharing', 'vacancy4', 'fees4'),
}


def _get_sharing_details(pg, sharing_type):
    sharing_flag, vacancy_field, fees_field = SHARING_FIELD_MAP[sharing_type]
    return sharing_flag, vacancy_field, fees_field, getattr(pg, vacancy_field) or 0, getattr(pg, fees_field)


def _restore_booking_seat(booking):
    _, vacancy_field, _, current_vacancy, _ = _get_sharing_details(booking.pg, booking.sharing_type)
    setattr(booking.pg, vacancy_field, current_vacancy + 1)
    booking.pg.save(update_fields=[vacancy_field])

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
    pgs = PGInformation.objects.filter(pguser=request.user)
    context = {
        'pgs': pgs,
        'show_empty_modal': not pgs.exists(),
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

# Booking Views
@login_required(login_url='login')
def book_pg(request, pk):
    try:
        pg = get_object_or_404(PGInformation, id=pk)
        
        # Check if user has already booked this PG
        existing_booking = Booking.objects.filter(user=request.user, pg=pg, status__in=['pending', 'confirmed']).first()
        if existing_booking:
            message = f'You already have a {existing_booking.status} booking for this PG.'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': message}, status=400)
            messages.warning(request, message)
            return redirect('my_bookings')

        if not pg.has_available_sharing():
            message = 'This PG is fully booked right now.'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': message}, status=400)
            messages.error(request, message)
            return redirect('pgdetails', pk=pk)
        
        if request.method == 'POST':
            form = BookingForm(request.POST, pg=pg)
            if form.is_valid():
                with transaction.atomic():
                    pg = PGInformation.objects.select_for_update().get(id=pk)
                    sharing_type = form.cleaned_data['sharing_type']
                    sharing_flag, vacancy_field, _, current_vacancy, fees = _get_sharing_details(pg, sharing_type)

                    if not getattr(pg, sharing_flag) or current_vacancy <= 0 or fees is None:
                        error_message = 'Selected sharing is no longer available. Please choose another option.'
                        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                            return JsonResponse({'success': False, 'error': error_message}, status=400)
                        messages.error(request, error_message)
                        return render(request, 'book_pg.html', {'form': BookingForm(pg=pg), 'pg': pg})

                    booking = form.save(commit=False)
                    booking.user = request.user
                    booking.pg = pg
                    booking.fees = fees
                    booking.status = 'confirmed'
                    booking.save()

                    setattr(pg, vacancy_field, current_vacancy - 1)
                    pg.save(update_fields=[vacancy_field])

                success_message = 'Booking completed successfully.'
                messages.success(request, success_message)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': success_message})
                return redirect('my_bookings')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': form.errors.as_text()}, status=400)
        else:
            form = BookingForm(pg=pg)
        
        return render(request, 'book_pg.html', {'form': form, 'pg': pg})
    
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('pgdetails', pk=pk)

@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'my_bookings.html', {'bookings': bookings, 'cancel_form': BookingCancellationForm()})

@login_required(login_url='login')
def manage_bookings(request):
    user_pgs = PGInformation.objects.filter(pguser=request.user)
    bookings = Booking.objects.filter(pg__in=user_pgs).order_by('-booking_date')
    context = {
        'bookings': bookings,
        'total_bookings': bookings.count(),
        'pending_bookings': bookings.filter(status='pending').count(),
        'confirmed_bookings': bookings.filter(status='confirmed').count(),
        'cancelled_bookings': bookings.filter(status='cancelled').count(),
    }
    return render(request, 'manage_bookings.html', context)

@login_required(login_url='login')
def update_booking_status(request, booking_id, status):
    try:
        with transaction.atomic():
            booking = Booking.objects.select_for_update().select_related('pg').get(id=booking_id)
            
            # Check if user owns the PG
            if booking.pg.pguser != request.user:
                return HttpResponse("You don't have permission to manage this booking")

            if status not in ['confirmed', 'cancelled', 'completed']:
                messages.error(request, 'Invalid status update')
                return redirect('manage_bookings')

            if booking.status == status:
                messages.info(request, f'Booking is already {status}.')
                return redirect('manage_bookings')

            if status == 'cancelled' and booking.status != 'cancelled':
                _restore_booking_seat(booking)

            booking.status = status
            booking.save(update_fields=['status'])
            messages.success(request, f'Booking {status} successfully!')

        return redirect('manage_bookings')
    
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('manage_bookings')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('manage_bookings')


@login_required(login_url='login')
def cancel_booking(request, booking_id):
    try:
        if request.method != 'POST':
            messages.error(request, 'Cancellation must be submitted from the form.')
            return redirect('my_bookings')

        form = BookingCancellationForm(request.POST)
        if not form.is_valid():
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)
            return redirect('my_bookings')

        with transaction.atomic():
            booking = Booking.objects.select_for_update().select_related('pg').get(id=booking_id, user=request.user)

            if booking.status == 'cancelled':
                messages.info(request, 'This booking is already cancelled.')
                return redirect('my_bookings')

            if booking.status == 'completed':
                messages.error(request, 'Completed bookings cannot be cancelled.')
                return redirect('my_bookings')

            _restore_booking_seat(booking)
            booking.status = 'cancelled'
            booking.cancellation_reason = form.cleaned_data['cancellation_reason']
            booking.save(update_fields=['status', 'cancellation_reason'])

        messages.success(request, 'Booking cancelled successfully. Your seat has been released.')
        return redirect('my_bookings')

    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('my_bookings')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('my_bookings')

@login_required(login_url='login')
def add_booking_review(request, booking_id):
    try:
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        # Check if booking is completed
        if booking.status != 'completed':
            messages.error(request, 'You can only review completed bookings.')
            return redirect('my_bookings')
        
        # Check if review already exists
        if hasattr(booking, 'bookingreview'):
            messages.warning(request, 'You have already reviewed this booking.')
            return redirect('my_bookings')
        
        if request.method == 'POST':
            form = BookingReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.booking = booking
                review.save()
                messages.success(request, 'Review submitted successfully!')
                return redirect('my_bookings')
        else:
            form = BookingReviewForm()
        
        return render(request, 'add_booking_review.html', {'form': form, 'booking': booking})
    
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('my_bookings')
