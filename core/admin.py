from django.contrib import admin
from .models import UserCredential, ZoomVideoCredential, ZoomYouTubeFile
from .forms import UserCrendentialAdminForm

# Register your models here.


@admin.register(UserCredential)
class UserCredentialAdmin(admin.ModelAdmin):
    form = UserCrendentialAdminForm
 

@admin.register(ZoomVideoCredential)
class ZoomVideoCredentialAdmin(admin.ModelAdmin):
    list_display = ['user', 'min_duration', 'from_day_delta', 'page_size']


@admin.register(ZoomYouTubeFile)
class ZoomYouTubeFileAdmin(admin.ModelAdmin):
    list_display = ['user', 'zoom_id', 'slug', 'zoom_name', 'zoom_video_file_url',
                    'youtube_video_file_url', 'youtube_link_status', 'appending_youtube_link_status',
                    'date_created', 'date_updated']