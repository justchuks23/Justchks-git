from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import ZoomYouTubeFile, UserCredential, ZoomVideoCredential


CustomUser = get_user_model()


class URLPatternTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.user_credentials = UserCredential.objects.create(
            user=self.user,
            zoom_email='test_email',
            zoom_client_id='test_client_id',
            zoom_client_secret='test_client_secret',
            zoom_account_id='test_account_id',
            google_email='test_email',
            google_client_id='test_client_id',
            google_client_secret='test_client_secret',
            google_code='test_code',
            google_refresh_token='test_refresh_token',
        )
        self.zoom_video = ZoomYouTubeFile.objects.create(
            user=self.user_credentials,
            zoom_id='test_zoom_id',
            zoom_name='Test Zoom Video',
            slug='test-zoom-video'
        )
        self.zoom_video_credential = ZoomVideoCredential.objects.create(
            user=self.user_credentials,
            min_duration=10,
            from_day_delta=7,
            page_size=10,
        )

    def test_admin_login_url(self):
        url = reverse('main:admin_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_logout_url(self):
        url = reverse('main:admin_logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Expected redirect

    def test_home_url(self):
        url = reverse('main:home', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_zoom_url(self):
        url = reverse('main:user_zoom', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Expected redirect

    def test_detail_url(self):
        url = reverse('main:detail', args=[self.zoom_video.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_upload_url(self):
        url = reverse('main:upload', args=[self.user.id, self.zoom_video.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

