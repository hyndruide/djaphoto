from django import forms
from django.core.exceptions import ValidationError
from .utils import verify_checksum
from django.forms import ModelForm
from .models import PhotoBooth,Authorization


class UploadForm(forms.Form):
    checksum = forms.CharField(label='checksum', max_length=100)
    name = forms.CharField(label='name', max_length=100)
    created_at = forms.CharField(label='name', max_length=100)
    file = forms.FileField()

    def clean(self):
        cleaned_data = super().clean()

        checksum = cleaned_data.get("checksum")
        fp = self.files["file"]

        if not verify_checksum(checksum, fp):
            raise ValidationError("invalid checksum")


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
