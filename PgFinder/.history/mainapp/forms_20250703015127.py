from django import forms

from .models import PGInformation,PGImage

class PGInformationForm(forms.ModelForm):
    class Meta:
        model=PGInformation
        fields='__all__'
        widgets={
            'two_sharing':forms.TextInput(attrs={'class':'two_sharing'}),

             'vaccancy2':forms.IntegerField(attrs={'class':'vaccancy2','disabled':'disabled'}),
             'fees1':forms.IntegerField(attrs={'class':'fees1','disabled':'disables'}),
             

            'three_sharing':forms.TextInput(attrs={'class':'three_sharing'}),
            'vaccancy3':forms.IntegerField(attrs={'class':'vaccancy3','disabled':'disabled'}),
            'fees1':forms.IntegerField(attrs={'class':'fees1','disabled':'disables'}),


            'four_sharing':forms.TextInput(attrs={'class':'four_sharing'}),
            'vaccancy4':forms.IntegerField(attrs={'class':'vaccancy4','disabled':'disabled'}),
            'fees1':forms.IntegerField(attrs={'class':'fees1','disabled':'disables'}),


            'other_sharing':forms.TextInput(attrs={'class':'other_sharing'}),
            'vaccancy':forms.IntegerField(attrs={'class':'vaccancy','disabled':'disabled'}),
            'fees1':forms.IntegerField(attrs={'class':'fees1','disabled':'disables'}),


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
            label='Upload Images'
            # required=True
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