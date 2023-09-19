import unittest
from unittest.mock import patch, MagicMock

from django.conf import settings

from .zoom import ZoomRecording, ZoomJWTClient


class ZoomJWTClientTestCase(unittest.TestCase):
    def test_setup(self):
        client = ZoomJWTClient(api_key='your_api_key', api_secret='your_api_secret', token_exp_delta=30)
        self.assertIsNotNone(client.access_token)
        self.assertIsNotNone(client.http_headers)

    def test_join_url(self):
        client = ZoomJWTClient(api_key='your_api_key', api_secret='your_api_secret', token_exp_delta=30)
        joined_url = client._join_url('/test')
        self.assertEqual(joined_url, 'https://api.zoom.us/v2/test')

    @patch('zoom.generate_access_token')
    @patch('zoom.make_http_headers')
    def test_init(self, mock_make_http_headers, mock_generate_access_token):
        api_key = 'your_api_key'
        api_secret = 'your_api_secret'
        token_exp_delta = 30

        client = ZoomJWTClient(api_key, api_secret, token_exp_delta)

        mock_generate_access_token.assert_called_once_with(api_key, api_secret, token_exp_delta)
        mock_make_http_headers.assert_called_once_with(mock_generate_access_token.return_value)
        self.assertEqual(client.api_key, api_key)
        self.assertEqual(client.api_secret, api_secret)
        self.assertEqual(client.token_exp_delta, token_exp_delta)
        self.assertEqual(client.access_token, mock_generate_access_token.return_value)
        self.assertEqual(client.http_headers, mock_make_http_headers.return_value)


class ZoomRecordingTestCase(unittest.TestCase):
    def setUp(self):
        self.client = ZoomJWTClient(api_key='your_api_key', api_secret='your_api_secret', token_exp_delta=30)
        self.email = 'test@example.com'
        self.recording = ZoomRecording(self.client, self.email)

    @patch('zoom.requests.get')
    def test_get_meetings(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'meetings': [
                {
                    'id': 'meeting_id',
                    'topic': 'Meeting Topic',
                    'duration': 15
                }
            ]
        }
        mock_get.return_value = mock_response

        meetings = self.recording.get_meetings()

        mock_get.assert_called_once_with(
            'https://api.zoom.us/v2/users/test@example.com/recordings?from=YYYY-MM-DD&page_size=10',
            headers=self.client.http_headers,
            timeout=60
        )
        self.assertEqual(len(meetings), 1)
        self.assertEqual(meetings[0]['topic'], 'Meeting Topic')
        self.assertEqual(meetings[0]['duration'], 15)

    def test_filter_meetings(self):
        meetings = [
            {
                'topic': 'Meeting 1',
                'duration': 5
            },
            {
                'topic': 'Meeting 2',
                'duration': 10
            },
            {
                'topic': 'Meeting 3',
                'duration': 20
            }
        ]
        self.recording.duration_min = 10
        filtered_meetings = list(self.recording.filter_meetings(meetings))
        self.assertEqual(len(filtered_meetings), 2)
        self.assertEqual(filtered_meetings[0]['topic'], 'Meeting 2')
        self.assertEqual(filtered_meetings[1]['topic'], 'Meeting 3')

    @patch('zoom.os.makedirs')
    @patch('zoom.requests.get')
    @patch('zoom.ZoomRecording._is_downloaded')
    @patch('zoom.ZoomRecording._real_download_file')
    @patch('zoom.ZoomRecording._save_to_db')
    def test_download_meetings(self, mock_save_to_db, mock_real_download_file, mock_is_downloaded,
                               mock_get, mock_makedirs):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'meetings': [
                {
                    'id': 'meeting_id',
                    'topic': 'Meeting Topic',
                    'start_time': '2023-06-01T10:00:00Z',
                    'recording_files': [
                        {
                            'id': 'file_id',
                            'file_type': 'MP4',
                            'download_url': 'https://example.com/video.mp4'
                        }
                    ]
                }
            ]
        }
        mock_is_downloaded.return_value = True
        mock_real_download_file.return_value = True

        save_dir = settings.VIDEO_DIR
        downloaded_files = 'backend/downloaded_files.txt'

        self.recording.download_meetings(save_dir, downloaded_files)

        mock_get.assert_called_once_with(
            'https://api.zoom.us/v2/users/test@example.com/recordings?from=YYYY-MM-DD&page_size=10',
            headers=self.client.http_headers,
            timeout=60
        )
        mock_makedirs.assert_called_once_with(save_dir)
        mock_real_download_file.assert_called_once_with(
            'https://example.com/video.mp4?access_token=mock_access_token',
            f'{settings.VIDEO_DIR}/Meeting Topic 01-06-2023.mp4'
        )
        mock_save_to_db.assert_called_once_with(downloaded_files, 'file_id',
                                                'https://example.com/video.mp4', 'Meeting Topic 01-06-2023.mp4')

    def test_is_downloaded_existing_file(self):
        downloaded_files = 'backend/downloaded_files.txt'
        with open(downloaded_files, 'w') as f:
            f.write('file_id1\nfile_id2\n')

        is_downloaded = self.recording._is_downloaded(downloaded_files, 'file_id1')
        self.assertFalse(is_downloaded)

    def test_is_downloaded_non_existing_file(self):
        downloaded_files = 'backend/downloaded_files.txt'
        with open(downloaded_files, 'w') as f:
            f.write('file_id1\nfile_id2\n')

        is_downloaded = self.recording._is_downloaded(downloaded_files, 'file_id3')
        self.assertTrue(is_downloaded)


if __name__ == '__main__':
    unittest.main()
