from django.contrib import admin
from .models import UserCredential, ZoomVideoCredential, TimeModel, ZoomYouTubeFile


# Register your models here.


@admin.register(UserCredential)
class UserCredentialAdmin(admin.ModelAdmin):
    list_display = ['user', 'zoom_email', 'zoom_client_id', 'zoom_client_secret',
                    'zoom_account_id', 'google_email', 'google_client_id', 'google_client_secret',
                    'google_code', 'google_refresh_token']


@admin.register(ZoomVideoCredential)
class ZoomVideoCredentialAdmin(admin.ModelAdmin):
    list_display = ['user', 'min_duration', 'from_day_delta', 'page_size']


@admin.register(TimeModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')



@admin.register(ZoomYouTubeFile)
class ZoomYouTubeFileAdmin(admin.ModelAdmin):
    list_display = ['user', 'zoom_id', 'slug', 'zoom_name', 'zoom_video_file_url',
                    'youtube_video_file_url', 'youtube_link_status', 'appending_youtube_link_status',
                    'date_created', 'date_updated']
