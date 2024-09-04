from django.db import models
from django.contrib.auth.models import Group
from django.urls import reverse

from django.utils.text import slugify
import uuid
from django.contrib.auth import get_user_model


# Create your models here.

CustomUser = get_user_model()


class UserCredential(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='credentials', null=True)
    zoom_email = models.EmailField(null=True, blank=True)
    zoom_client_id = models.CharField(max_length=256, null=True, blank=True)
    zoom_client_secret = models.CharField(max_length=256, null=True, blank=True)
    zoom_account_id = models.CharField(max_length=256, null=True, blank=True)
    google_email = models.EmailField(null=True, blank=True)
    google_client_id = models.CharField(max_length=256, null=True, blank=True)
    google_client_secret = models.CharField(max_length=256, null=True, blank=True)
    google_code = models.CharField(max_length=256, null=True, blank=True)
    google_refresh_token = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.pk is None:
            group, _ = Group.objects.get_or_create(name='Officials')
            self.user.groups.add(group)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.groups.clear()
        self.user.user_permissions.clear()
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:home', args=[self.user.id])
    

class TimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  


class TimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  


class ZoomVideoCredential(models.Model):
    user = models.ForeignKey(UserCredential, on_delete=models.CASCADE, related_name='credential_get_zoom', null=True)
    min_duration = models.IntegerField(default=10, null=True, blank=True)
    from_day_delta = models.IntegerField(default=7, null=True, blank=True)
    page_size = models.IntegerField(default=10, null=True, blank=True)

    def __str__(self):
        return f"{self.user}"


class ZoomYouTubeFile(models.Model):
    user = models.ForeignKey(UserCredential, on_delete=models.CASCADE, related_name='credential_zoom', null=True)
    zoom_id = models.CharField(max_length=256, null=True, blank=True, unique=True)
    slug = models.SlugField(max_length=256, unique=True, blank=True)
    zoom_name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Zoom name', default='Not available')
    zoom_video_file_url = models.URLField(max_length=800, verbose_name='Zoom video link', blank=True, null=True, default='Not available')
    youtube_video_file_url = models.URLField(verbose_name='YouTube video link', null=True, blank=True)
    youtube_link_status = models.BooleanField(default=False, verbose_name='YouTube link status')
    appending_youtube_link_status = models.BooleanField(default=False, verbose_name='Appending status')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_created"]
        verbose_name_plural = "Zoom Youtube Files"
            
    def __str__(self):
        return f'{self.zoom_id}'

    def get_absolute_url(self):
        return reverse('main:detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.zoom_id)
        super().save(*args, **kwargs)
    