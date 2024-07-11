from django import forms
from django.contrib.auth.forms import AuthenticationForm


class AdminLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ZoomYoutubeUploadForm(forms.Form):
    zoom_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Zoom ID'
    )


class UploadYoutubeForm(forms.Form):
    user_id = forms.IntegerField()
    zoom_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Zoom ID'
    )


