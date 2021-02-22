from django import forms
from django.core.exceptions import ValidationError
from .utils import verify_checksum
from django.forms import ModelForm
from .models import PhotoBooth,Authorization




class ValidateBooth(forms.Form):
    user_code = forms.CharField(label='Code', max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

    def clean_user_code(self):
        data = self.cleaned_data['user_code']
        data = data.replace("-", "")
        if len(data) != 8:
            raise ValidationError("Un code contient 8 caractères")
        elif not Authorization.objects.filter(user_code=data).exists():
            raise ValidationError("Ce code n'existe pas")
        return data.replace("-", "")

class PhotoBoothForm(ModelForm):
    class Meta:
        model = PhotoBooth
        fields = ['nom']

