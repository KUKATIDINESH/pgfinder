from django import forms
from django.forms.widgets import FileInput
from .models import PGInformation, PGImage, Booking, BookingReview

class PGInformationForm(forms.ModelForm):
    class Meta:
        model=PGInformation
        fields='__all__'
        exclude=['pguser']
        widgets={
            'two_sharing':forms.CheckboxInput(attrs={'class':'two_sharing'}),
             'vacancy2':forms.NumberInput(attrs={'class':'vacancy2'}),
             'fees2':forms.NumberInput(attrs={'class':'fees2'}),
            'three_sharing':forms.CheckboxInput(attrs={'class':'three_sharing'}),
            'vacancy3':forms.NumberInput(attrs={'class':'vacancy3'}),
            'fees3':forms.NumberInput(attrs={'class':'fees3'}),
            'four_sharing':forms.CheckboxInput(attrs={'class':'four_sharing'}),
            'vacancy4':forms.NumberInput(attrs={'class':'vacancy4'}),
            'fees4':forms.NumberInput(attrs={'class':'fees4'}),
            'other_sharing':forms.CheckboxInput(attrs={'class':'other_sharing'}),
            'vacancy':forms.NumberInput(attrs={'class':'vacancy'}),
            'fees':forms.NumberInput(attrs={'class':'fees'}),
            # Facilities checkboxes
            'washing_machine':forms.CheckboxInput(attrs={'class':'facility-checkbox'}),
            'water_heater':forms.CheckboxInput(attrs={'class':'facility-checkbox'}),
            'ac':forms.CheckboxInput(attrs={'class':'facility-checkbox'}),
            'bathroom_type':forms.Select(choices=PGInformation.BATHROOM_CHOICES),
            'area':forms.Select(choices=PGInformation.AREA_CHOICES),
            'address':forms.Textarea(attrs={'rows':3, 'cols':50}),
        }

class MultipleFileInput(FileInput):
    allow_multiple_selected = True

class PGImageUploadForm(forms.Form):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True,}),
        label='Upload Images',
        required=False
    )

# Booking Forms
class BookingForm(forms.ModelForm):
    SHARING_CHOICES = Booking.SHARING_CHOICES
    
    sharing_type = forms.ChoiceField(choices=SHARING_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    contact_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your contact number'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Any special requirements or messages...'}), required=False)
    
    class Meta:
        model = Booking
        fields = ['sharing_type', 'start_date', 'end_date', 'contact_number', 'message']
        
    def __init__(self, *args, **kwargs):
        self.pg = kwargs.pop('pg', None)
        super().__init__(*args, **kwargs)
        
        if self.pg:
            available_choices = []
            if self.pg.other_sharing and (self.pg.vacancy or 0) > 0:
                available_choices.append(('single', 'Single Sharing'))
            if self.pg.two_sharing and (self.pg.vacancy2 or 0) > 0:
                available_choices.append(('double', '2 Sharing'))
            if self.pg.three_sharing and (self.pg.vacancy3 or 0) > 0:
                available_choices.append(('triple', '3 Sharing'))
            if self.pg.four_sharing and (self.pg.vacancy4 or 0) > 0:
                available_choices.append(('four', '4 Sharing'))
            self.fields['sharing_type'].choices = available_choices

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date must be after start date")
            
            # Check if start date is not in the past
            from datetime import date
            if start_date < date.today():
                raise forms.ValidationError("Start date cannot be in the past")
        
        return cleaned_data

    def clean_sharing_type(self):
        sharing_type = self.cleaned_data.get('sharing_type')
        valid_choices = {choice[0] for choice in self.fields['sharing_type'].choices}
        if sharing_type not in valid_choices:
            raise forms.ValidationError("Please select an available sharing type.")
        return sharing_type

class BookingReviewForm(forms.ModelForm):
    class Meta:
        model = BookingReview
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)], attrs={'class': 'form-control'}),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience...'}),
        }


class BookingCancellationForm(forms.Form):
    cancellation_reason = forms.CharField(
        min_length=5,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us why you want to cancel this booking',
            }
        ),
    )
