import os.path

from datetime import datetime
from datetime import timedelta
from urllib.parse import urljoin

import requests

from .server_oauth import make_http_headers, generate_jwt_token, generate_access_token, make_jwt_payload
from core.models import generate_unique_slug
from core.models import ZoomYouTubeFile, UserCredential

"""
ZoomJWTClient class is used for authentication of the zoom credentials
using the jwt_auth function parameters.
"""


class ZoomJWTClient(object):
    BASE_URL = 'https://api.zoom.us/v2/'

    def __init__(self, client_id: str, client_secret: str, account_id: str, token_exp_delta: int):
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_exp_delta = token_exp_delta

        self._setup()

    def _setup(self):
        authorization_token = generate_jwt_token(make_jwt_payload(self.client_id, self.token_exp_delta), self.client_secret)
        self.access_token = generate_access_token(
            self.account_id,
            authorization_token
        )
        self.http_headers = make_http_headers(self.access_token)

    def _join_url(self, path):
        if path.startswith('/'):
            path = path[1:]
        return urljoin(self.BASE_URL, path)

    def get(self, uri: str, **kwargs):
        url = self._join_url(uri)
        resp = requests.get(url, headers=self.http_headers, timeout=60)
        return resp


"""
ZoomRecording class performs the major tasks with the following:
1. Get the meetings from number of days - 7 days
2. Filter the meetings that has a minimum duration of 10 minutes video
3. Download the filtered video recordings and store in 2 directories (video_dir and download_dir)
4. Download_dir saves the recording_id and the video files
5. Video_dir saves the url to the video and the video files
6. Stores the download_dir to database with id

NOTE: call a model class to save the videos to database in the _save_to_db function or put this in models
"""


class ZoomRecording(object):
    def __init__(self, client, email, duration_min=10, filter_meeting_by_name=False,
                 only_meeting_names=None, from_day_delta=7, page_size=10):

        self.client = client
        self.email = email

        self.duration_min = duration_min
        self.filter_meeting_by_name = filter_meeting_by_name
        self.only_meeting_names = only_meeting_names or []
        self.from_day_delta = from_day_delta
        self.page_size = page_size

    def get_meetings(self):
        """ Changed from page_size to self.page_size """

        uri = f"users/{self.email}/recordings?from={(datetime.utcnow() - timedelta(days=self.from_day_delta)).strftime('%Y-%m-%d')}&page_size={self.page_size}"
        resp = self.client.get(uri)
        if resp.status_code != 200:
            print(f"Get meeting status error: {resp.status_code}. Detail: {resp.content}")
            return None

        data = resp.json()
        return data.get('meetings', [])

    def filter_meetings(self, meetings):
        for m in meetings:
            if m.get("duration", 0) < self.duration_min:
                continue

            if self.filter_meeting_by_name and m.get("topic").strip() not in self.only_meeting_names:
                continue

            yield m

    def download_meetings(self, user, save_dir, downloaded_files):
        meetings = self.get_meetings()
        if not meetings:
            print("Does not exists meetings.")
            return
        """
        getting the recorded files (MP4) and storing in a variable (recorded_files),
        for each meeting. A meeting can have MP4, MA4, TXT files
        """
        meetings = self.filter_meetings(meetings)
        for meeting in meetings:
            recording_files = filter(
                lambda x: x.get("file_type") == "MP4", meeting.get('recording_files', [])
            )
            for i, video_data in enumerate(recording_files):
                rid = video_data.get('id')

                """
                returns True if the rid is already there, hence skip to saving to database
                """
                if not self._is_downloaded(downloaded_files, rid):
                    continue

                prefix = i or ''
                filename = self._get_output_filename(meeting, prefix)
                save_path = self._get_output_path(filename, save_dir)

                if os.path.exists(save_path):
                    print(f"File already exists: {video_data.get('download_url')}. Skipping to download the next one.")
                    continue

                download_url = video_data.get('download_url')
                download_url += f"?access_token={self.client.access_token}"

                self._real_download_file(download_url, save_path)

                print(f"Downloaded the file: {video_data.get('download_url')}")

                self._save_to_db(user, downloaded_files, rid, download_url, filename)

    def _is_downloaded(self, downloaded_files, recording_id):
        if not os.path.exists(downloaded_files):
            return True

        with open(downloaded_files, 'r') as f:
            ids = [x.strip() for x in f.readlines() if x]

        if recording_id in ids:
            return False

        return True

    def _get_output_filename(self, meeting, prefix=''):
        start_time = datetime.strptime(
            meeting.get('start_time'), '%Y-%m-%dT%H:%M:%SZ'
        ).strftime('%d-%m-%Y')
        topic = meeting.get('topic').replace('/', '.')
        return f'{topic}{prefix} {start_time}.mp4'

    def _get_output_path(self, fname, save_dir):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        return os.path.join(save_dir, fname)

    def _real_download_file(self, url, fpath):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(fpath.encode('utf-8'), 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        return False

    # this saves the downloaded zoom video files to database

    def _save_to_db(self, user, downloaded_files, recording_id, video_url, filename):
        
        with open(downloaded_files, 'a+') as zoom_video_files:
            zoom_video_files.write('{}\n'.format(recording_id))
            for file in downloaded_files:
                title = file['title']
                unique_slug = generate_unique_slug(title)
        # this saves the video from local storage to database using the models
        zoom_download_url_database = ZoomYouTubeFile.objects.create(
            title=title,
            user=user,
            zoom_id=recording_id, zoom_video_file_url=video_url,
            zoom_name=filename,
            slug = unique_slug
        )
        zoom_download_url_database.save()

    