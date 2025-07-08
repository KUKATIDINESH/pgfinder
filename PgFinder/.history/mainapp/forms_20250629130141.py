from django import forms

from .models import PGInformation,PGImage

class PGInformationForm(forms.ModelForm):
    class Meta:
        model=PGInformation
        fields='__all__'
        widgets={
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
            widget=MultipleFileInput(attrs={'multiple': True}),
            label='Upload Images',name=''
            # required=True
        )


        def save(self, pg_instance, commit=True):
            files = self.files.getlist('images')
            instances = []
            for f in files:
                instance = PGImage(pg=pg_instance, image=f)
                if commit:
                    instance.save()
                instances.append(instance)
            return instances