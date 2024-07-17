from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserCredential

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserCrendentialAdminForm(forms.ModelForm):
    user_credentials = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta: 
        model = UserCredential
        fields=['zoom_client_id', 'zoom_client_secret',
                'zoom_account_id', 'google_client_id', 'google_client_secret',
                'google_code', 'google_refresh_token']


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


