import os.path
from unittest.mock import patch

from django.conf import settings
from django.contrib import messages
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
from core.models import UserCredential, ZoomYouTubeFile, ZoomVideoCredential
from core.forms import AdminLoginForm, ZoomYoutubeUploadForm, UploadYoutubeForm
from core.cron import run_user_zoom_downloader
from src.get_google_refresh_token import get_token
from core.tasks import upload_to_youtube_from_dir

CustomUser = get_user_model()


class AdminLoginViewTestCase(TestCase):
    def test_admin_login_view_get(self):
        response = self.client.get(reverse('main:admin_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forms/login.html')
        self.assertIsInstance(response.context['admin_user_form'], AdminLoginForm)

    def test_admin_login_view_post_valid(self):
        user = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            is_staff=True
        )
        data = {'username': 'admin', 'password': 'adminpassword'}
        response = self.client.post(reverse('main:admin_login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:home', args=[user.id]))

    def test_admin_login_view_post_invalid(self):
        data = {'username': 'admin', 'password': 'invalidpassword'}
        response = self.client.post(reverse('main:admin_login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:admin_login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid Password or Username')


class ZoomVideoListViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_zoom_video_list_view(self):
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/dashboard.html')
        self.assertEqual(len(response.context['zoom_files']), 0)  # Assuming no ZoomYouTubeFile instances exist

    # Add more test cases for ZoomVideoListView as needed


class GetZoomVideoViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.user_credential = UserCredential.objects.create(
            user=self.client.user,
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

        self.zoom_video_credential = ZoomVideoCredential.objects.create(
            user=self.user_credential,
            min_duration=10,
            from_day_delta=7,
            page_size=10,
        )

    def text_get_method_redirect(self):
        response = self.client.get(reverse('main:user_zoom', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:home', args=[self.user.id]))

    @patch('core.cron.run_user_zoom_downloader.delay')
    def test_post_method_success(self, mock_run_user_zoom_downloader):
        response = self.client.post(reverse('main:user_zoom', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:home', args=[self.user.id]))

        mock_run_user_zoom_downloader.assert_called_once_with({
            'user_id': self.user.id,
            'zoom_client_id': self.user_credential.zoom_client_id,
            'zoom_client_secret': self.user_credential.zoom_client_secret,
            'zoom_account_id': self.user_credential.zoom_account_id,
            'zoom_email': self.user_credential.zoom_email,
            'min_duration': self.zoom_video_credential.min_duration,
            'from_day_delta': self.zoom_video_credential.from_day_delta,
            'page_size': self.zoom_video_credential.page_size
        })

        message_list = [str(msg) for msg in messages.get_messages(response.wsgi_request)]
        self.assertIn('Video Downloading, wait a minute', message_list)

    def test_post_method_failure(self):
        response = self.client.post(reverse('main:user_zoom', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('main:home', args=[self.user.id]))

        message_list = [str(msg) for msg in messages.get_messages(response.wsgi_request)]
        self.assertIn('Video Downloading Failed. User do not exist', message_list)


class ZoomVideoDisplayViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.user_credential = UserCredential.objects.create(
            user=self.client.user,
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
            user=self.user_credential,
            zoom_id='zoom_id',
            zoom_name='zoom_name',
            zoom_video_file_url='zoom_video_file_url',
            youtube_video_file_url='youtube_video_file_url',
            youtube_link_status=False,
            appending_youtube_link_status=False,
        )

    def test_get_method(self):
        response = self.client.get(reverse('main:detail', args=[self.zoom_video.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/detail.html')
        self.assertEqual(response.context['zoom_video'], self.zoom_video)
        self.assertIsInstance(response.context['form'], ZoomYoutubeUploadForm)


class ZoomVideoFormViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.user_credential = UserCredential.objects.create(
            user=self.client.user,
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
            user=self.user_credential,
            zoom_id='zoom_id',
            zoom_name='zoom_name',
            zoom_video_file_url='zoom_video_file_url',
            youtube_video_file_url='youtube_video_file_url',
            youtube_link_status=False,
            appending_youtube_link_status=False,
        )

    @patch('src.get_google_refresh_token.get_token.delay')
    def test_post_method_no_refresh_token(self, mock_get_token):
        mock_get_token.return_value = {
            'error_description': 'Test error message'
        }
        data = {'zoom_id': self.zoom_video.zoom_id}
        response = self.client.post(reverse('main:upload', args=[self.user.id, self.zoom_video.id]), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:upload', args=[self.user.id, self.zoom_video.id]))

        message_list = [str(msg) for msg in messages.get_messages(response.wsgi_request)]
        self.assertIn('Sorry! could not process your request. Contact the Admin shortly. Test error message', message_list)
        self.zoom_video.refresh_from_db()
        self.assertTrue(self.zoom_video.appending_youtube_link_status)

    @patch('src.get_google_refresh_token.get_token.delay')
    def test_post_method_refresh_token(self, mock_get_token):
        mock_get_token.return_value = None
        data = {'zoom_id': self.zoom_video.zoom_id}
        response = self.client.post(reverse('main:upload', args=[self.user.id, self.zoom_video.id]), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:upload', args=[self.user.id, self.zoom_video.id]))

        messages_list = [str(msg) for msg in messages.get_messages(response.wsgi_request)]
        self.assertIn('Success generating a token', messages_list)
        self.zoom_video.refresh_from_db()
        self.assertTrue(self.zoom_video.appending_youtube_link_status)


class ZoomVideoDetailViewTestCase(TestCase):
    def test_get_method(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        zoom_video = ZoomYouTubeFile.objects.create(
            user=user,
            zoom_id='test_zoom_id',
            zoom_name='Test Zoom Video',
        )

        response = self.client.get(reverse('main:zoom_video_detail', args=[user.id, zoom_video.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/details.html')


class UploadDisplayViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.user_credential = UserCredential.objects.create(
            user=self.client.user,
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
            user=self.user_credential,
            zoom_id='zoom_id',
            zoom_name='zoom_name',
            zoom_video_file_url='zoom_video_file_url',
            youtube_video_file_url='youtube_video_file_url',
            youtube_link_status=False,
            appending_youtube_link_status=True,
        )

    def test_get_method(self):
        response = self.client.get(reverse('main:upload', args=[self.user.id, self.zoom_video.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/confirm.html')
        self.assertEqual(response.context['zoom_video'], self.zoom_video)
        self.assertIsInstance(response.context['form'], UploadYoutubeForm)


class UploadFormViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.user_credential = UserCredential.objects.create(
            user=self.client.user,
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
            user=self.user_credential,
            zoom_id='zoom_id',
            zoom_name='zoom_name',
            zoom_video_file_url='zoom_video_file_url',
            youtube_video_file_url='youtube_video_file_url',
            youtube_link_status=False,
            appending_youtube_link_status=True,
        )

    @patch('core.tasks.upload_to_youtube_from_dir.delay')
    def test_post_method_success(self, mock_upload_to_youtube_from_dir):
        mock_upload_to_youtube_from_dir.return_value = 'https://www.youtube.com/watch?v=test_video_id'
        video_file_path = os.path.join(settings.MEDIA_ROOT, self.zoom_video.zoom_id)
        data = {
            'user_id': self.user.id,
            'zoom_id': self.zoom_video.zoom_name,
        }
        response = self.client.post(reverse('main:upload', args=[self.user.id, self.zoom_video.slug]), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:home', args=[self.user.id]))
        messages_list = [str(msg) for msg in messages.get_messages(response.wsgi_request)]
        self.assertIn('Video uploaded successfully to YouTube', messages_list)

        self.zoom_video.refresh_from_db()
        self.assertTrue(self.zoom_video.youtube_link_status)
        self.assertEqual(self.zoom_video.youtube_video_file_url, 'https://www.youtube.com/watch?v=test_video_id')

    @patch('main.views.upload_to_youtube_from_dir.delay')
    def test_post_method_upload_error(self, mock_upload_to_youtube_from_dir):
        mock_upload_to_youtube_from_dir.return_value = ''
        video_file_path = os.path.join(settings.MEDIA_ROOT, self.zoom_video.zoom_id)

        data = {
            'user_id': self.user.id,
            'zoom_id': self.zoom_video.zoom_name,
        }
        response = self.client.post(reverse('main:upload', args=[self.user.id, self.zoom_video.slug]), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:upload', args=[self.user.id, self.zoom_video.slug]))

        messages_list = [str(msg) for msg in messages.get_messages(response.wsgi_request)]
        self.assertIn('Error uploading the video', messages_list)

    # Add more test cases for UploadFormView as needed


class UploadDetailViewTestCase(TestCase):
    def test_get_method(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        zoom_video = ZoomYouTubeFile.objects.create(
            user=user,
            zoom_id='test_zoom_id',
            zoom_name='Test Zoom Video',
            slug='test-zoom-video'
        )

        response = self.client.get(reverse('main:upload', args=[user.id, zoom_video.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forms/confirm.html')
