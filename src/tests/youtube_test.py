import datetime
import os
import unittest
from unittest.mock import patch

from django.conf import settings

from .youtube import YoutubeClient, FFMpegHandler, YoutubeRecording


class YoutubeClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client_id = 'your_client_id'
        self.client_secret = 'your_client_secret'
        self.refresh_token = 'your_refresh_token'
        self.client = YoutubeClient(self.client_id, self.client_secret, self.refresh_token)

    def test_get_auth_code(self):
        # Mock the requests.post method to return a response with access_token
        with patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {'access_token': 'test_access_token'}
            auth_code = self.client.get_auth_code()
            mock_post.assert_called_once_with(
                'https://accounts.google.com/o/oauth2/token',
                data={
                    'refresh_token': self.refresh_token,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'grant_type': 'refresh_token',
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json',
                }
            )
            self.assertEqual(auth_code, 'test_access_token')

    def test_get_authenticated_service(self):
        # Mock AccessTokenCredentials and build to avoid making actual API calls
        with patch('youtube.build') as mock_build:
            credentials_mock = mock_build.return_value
            service = self.client.get_authenticated_service()
            mock_build.assert_called_once_with(
                'youtube', 'v3', http=credentials_mock.authorize.return_value
            )
            self.assertEqual(service, credentials_mock)


class FFMpegHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.video_handler = FFMpegHandler()

    @patch('youtube.call')
    @patch('os.remove')
    @patch('os.rename')
    def test_start(self, mock_rename, mock_remove, mock_call):
        video_dir = settings.VIDEO_DIR
        fpath = os.path.join(video_dir, 'video.mp4')
        out_fpath = os.path.join(video_dir, 'out.mp4')
        self.video_handler.start(video_dir, fpath)
        mock_call.assert_called_once_with([
            'ffmpeg', '-i', fpath, '-crf', '18', '-preset', 'veryfast', '-c:a', 'copy', out_fpath
        ])
        mock_remove.assert_called_once_with(fpath)
        mock_rename.assert_called_once_with(out_fpath, fpath)


class YoutubeRecordingTestCase(unittest.TestCase):
    def setUp(self):
        self.client_id = 'your_client_id'
        self.client_secret = 'your_client_secret'
        self.refresh_token = 'your_refresh_token'
        self.video_dir = settings.VIDEO_DIR
        self.recording = YoutubeRecording(self.client_id, self.client_secret, self.refresh_token)

    @patch('youtube.YoutubeClient')
    @patch('youtube.FFMpegHandler')
    def test_upload_from_dir(self, mock_handler, mock_client):
        mock_client.return_value.get_authenticated_service.return_value = 'mock_service'
        mock_handler.return_value.start.return_value = None
        video_url = self.recording.upload_from_dir(self.video_dir)
        mock_handler.return_value.start.assert_not_called()
        self.assertIsNone(video_url)

        # Add more test cases for different scenarios
    @patch('youtube.YoutubeClient')
    @patch('youtube.FFMpegHandler')
    def test_send_notification(self, mock_handler, mock_client):
        mock_client.return_value.get_authenticated_service.return_value = 'mock_service'
        mock_handler.return_value.start.return_value = None

        payload = {
            'success': True,
            'result': {
                'name': 'Test Video',
                'link': 'https://www.youtube.com/watch?v=abc123',
                'date': datetime.datetime.now(),
            },
        }

        with patch('youtube.YoutubeRecording._send_notification') as mock_send_notification:
            self.recording.upload_from_dir(self.video_dir, notify=True)
            mock_send_notification.assert_called_once_with(payload)


if __name__ == '__main__':
    unittest.main()
