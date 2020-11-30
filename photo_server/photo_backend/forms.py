from django import forms
from django.core.exceptions import ValidationError
from .utils import verify_checksum


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
    Code = forms.CharField(label='Code', max_length=100)
