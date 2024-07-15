from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserCredential

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ZoomYoutubeUploadForm(forms.Form):
    zoom_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Zoom ID'
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password-input'}))

class UserCrendentialFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserCrendentialFileForm, self).__init__(args, **kwargs)
        self.fields['zoom_client_id', 'zoom_client_secret']

    class Meta: 
        model = UserCredential
        exclude = ('slug',)

class UploadYoutubeForm(forms.Form):
    user_id = forms.IntegerField()
    zoom_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Zoom ID'
    )


