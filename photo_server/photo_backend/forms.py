from django import forms


class UploadForm(forms.Form):
    checksum = forms.CharField(label='checksum', max_length=100)
    name = forms.CharField(label='name', max_length=100)
    created_at = forms.CharField(label='name', max_length=100)
    file = forms.FileField()


class ValidateBooth(forms.Form):
    Code = forms.CharField(label='Code', max_length=100)
