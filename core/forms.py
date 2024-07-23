from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserCredential

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserCrendentialAdminForm(forms.ModelForm):
    zoom_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    zoom_client_id = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    zoom_client_secret = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'control'})
    )
    zoom_account_id = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    google_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    google_client_id = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}) 
    )
    google_client_secret = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})
    ) 
    google_code = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})    
    )
    google_refresh_token = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})  
    )

    class Meta:
        model = UserCredential
        fields=['zoom_email', 'zoom_client_id', 'zoom_client_secret',
                'zoom_account_id', 'google_email', 'google_client_id', 'google_client_secret',
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


