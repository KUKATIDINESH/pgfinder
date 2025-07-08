from django import forms

from .models import PGInformation,PGImage

class PGInformationForm(forms.ModelForm):
    class Meta:
        model=PGInformation
        fields=
        exclude=['pguser']
        widgets={
            'two_sharing':forms.CheckboxInput(attrs={'class':'two_sharing'}),

             'vacancy2':forms.NumberInput(attrs={'class':'vacancy2','disabled':'disabled'}),
             'fees2':forms.NumberInput(attrs={'class':'fees2','disabled':'disabled'}),
             

            'three_sharing':forms.CheckboxInput(attrs={'class':'three_sharing'}),
            'vacancy3':forms.NumberInput(attrs={'class':'vacancy3','disabled':'disabled'}),
            'fees3':forms.NumberInput(attrs={'class':'fees3','disabled':'disabled'}),


            'four_sharing':forms.CheckboxInput(attrs={'class':'four_sharing'}),
            'vacancy4':forms.NumberInput(attrs={'class':'vacancy4','disabled':'disabled'}),
            'fees4':forms.NumberInput(attrs={'class':'fees4','disabled':'disabled'}),


            'other_sharing':forms.CheckboxInput(attrs={'class':'other_sharing'}),
            'vacancy':forms.NumberInput(attrs={'class':'vacancy','disabled':'disabled'}),
            'fees':forms.NumberInput(attrs={'class':'fees','disabled':'disabled'}),


            'password':forms.PasswordInput(),
            'bathroom_type':forms.Select(choices=PGInformation.BATHROOM_CHOICES),
            'area':forms.Select(choices=PGInformation.AREA_CHOICES),
            'address':forms.Textarea(attrs={'rows':3, 'cols':50}),
        }

from django.forms.widgets import FileInput
class MultipleFileInput(FileInput):
        allow_multiple_selected = True



    

class PGImageUploadForm(forms.Form):
        images = forms.FileField(
            widget=MultipleFileInput(attrs={'multiple': True,}),
            label='Upload Images',
            required=False
        )

        # def save(self, pg_instance, commit=True):
        #     images= self.cleaned_data.get('images')
        #     if not images:
        #         return []
        #     if isinstance(images,list):
        #          files=images
        #     instances = []
        #     for f in files:
        #         instance = PGImage(pg=pg_instance, image=f)
        #         if commit:
        #             instance.save()
        #         instances.append(instance)
        #     return instances