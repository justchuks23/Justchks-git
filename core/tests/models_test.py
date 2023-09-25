from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import datetime

from core.models import UserCredential, ZoomVideoCredential, ZoomYouTubeFile


CustomUser = get_user_model()


class UserCredentialTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_user_credential_creation(self):
        user_credential = UserCredential.objects.create(
            user=self.user,
            zoom_email='test@example.com',
            zoom_client_id='zoom_client_id',
            zoom_client_secret='zoom_client_secret',
            zoom_account_id='zoom_account_id',
            google_email='test@example.com',
            google_client_id='google_client_id',
            google_client_secret='google_client_secret',
            google_code='google_code',
            google_refresh_token='google_refresh_token',
        )
        self.assertEqual(user_credential.user, self.user)
        self.assertTrue(UserCredential.objects.filter(user=self.user).exists())


class ZoomVideoCredentialTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.user_credential = UserCredential.objects.create(user=self.user)

    def test_zoom_video_credential_creation(self):
        zoom_video_credential = ZoomVideoCredential.objects.create(
            user=self.user_credential,
            min_duration=10,
            from_day_delta=7,
            page_size=10,
        )
        self.assertEqual(zoom_video_credential.user, self.user_credential)
        self.assertTrue(ZoomVideoCredential.objects.filter(user=self.user_credential).exists())


class ZoomYouTubeFileTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.user_credential = UserCredential.objects.create(user=self.user)

    def test_zoom_youtube_file_creation(self):
        zoom_youtube_file = ZoomYouTubeFile.objects.create(
            user=self.user_credential,
            zoom_id='zoom_id',
            slug='slug',
            zoom_name='zoom_name',
            zoom_video_file_url='zoom_video_file_url',
            youtube_video_file_url='youtube_video_file_url',
            youtube_link_status=True,
            appending_youtube_link_status=True,
            date_created=datetime.now(),
            date_updated=datetime.now()
        )
        self.assertEqual(zoom_youtube_file.user, self.user_credential)
        self.assertTrue(ZoomYouTubeFile.objects.filter(user=self.user_credential).exists())
        # Add more assertions for other fields

    def test_zoom_youtube_file_slug_generation(self):
        zoom_youtube_file = ZoomYouTubeFile.objects.create(
            user=self.user_credential,
            zoom_id='zoom_id',
            # Add other required fields
        )
        self.assertEqual(zoom_youtube_file.slug, 'zoom_id')  # Assert slug generation

    # Add more test cases as needed

