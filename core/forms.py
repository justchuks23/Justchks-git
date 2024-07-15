from django import forms
from django.contrib.auth.forms import AuthenticationForm


class AdminLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ZoomYoutubeUploadForm(forms.Form):
    class Meta:
        model = ZoomYouTubeFile
        zoom_id = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            label='Zoom ID'
        )
        password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password-input'}))

class UploadYoutubeForm(forms.Form):
    user_id = forms.IntegerField()
    zoom_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Zoom ID'
    )


