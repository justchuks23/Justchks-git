# -*- coding: utf-8 -*-

import os
import random
import time
import re

import httplib2
import requests

try:
    import httplib
except ImportError:
    import http.client as httplib

from subprocess import call

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import AccessTokenCredentials

from django.conf import settings

import logging

# logging the information
logging_info = logging.getLogger(__name__)

# Explicitly tell the underlying HTTP transport library not to retry,
# since we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error, IOError, httplib.NotConnected,
    httplib.IncompleteRead, httplib.ImproperConnectionState,
    httplib.CannotSendRequest, httplib.CannotSendHeader,
    httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError
# with one of these status codes is raised.
RETRIABLE_STATUS_CODES = (500, 502, 503, 504)


class YoutubeClient(object):
    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

    def get_auth_code(self):
        """ Get access token for connect to YouTube api """
        oauth_url = 'https://accounts.google.com/o/oauth2/token'
        data = dict(
            refresh_token=self.refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type='refresh_token',
        )

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        response = requests.post(oauth_url, data=data, headers=headers)
        response = response.json()
        return response.get('access_token')

    def get_authenticated_service(self):
        """ Create YouTube oauth2 connection """
        credentials = AccessTokenCredentials(
            access_token=self.get_auth_code(),
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        )
        return build(
            'youtube', 'v3', http=credentials.authorize(httplib2.Http())
        )


class FFMpegHandler(object):

    def start(self, video_dir, fpath):
        out_fpath = os.path.join(video_dir, 'out.mp4')
        call([
            'ffmpeg', '-i', fpath, '-crf', '18', '-preset', 'veryfast', '-c:a', 'copy', out_fpath
        ])
        os.remove(fpath)
        os.rename(out_fpath, fpath)


class YoutubeRecording(object):
    def __init__(self,
                 client_id,
                 client_secret,
                 refresh_token,
                 video_handler_class=FFMpegHandler):
        self.client = YoutubeClient(client_id, client_secret, refresh_token)
        self.video_handler = video_handler_class()

    def upload_from_dir(self, video_path: str,
                        title: str,
                        privacy_status='unlisted',
                        notify=True,
                        remove_file=False):
        """
        Uploads a video to YouTube.

        :param notify:
        :param remove_file:
        :param video_path: The file path to the video file.
        :param title: The title of the video.
        :param privacy_status: The privacy status of the video (default: 'unlisted').
        :return: The YouTube video URL.
        """

        video_file_path = os.path.abspath(video_path)

        if not os.path.exists(video_file_path):
            raise FileNotFoundError(f"File not found in this directory: {video_path}")

        if settings.ENABLE_VIDEO_CONVERTING:
            self.video_handler.start(os.path.dirname(video_path), video_path)

        title = self.modify_title(title)

        option = dict(
            file=video_path,
            title=title,
            privacyStatus=privacy_status
        )

        video_id = self.upload_video(option)

        if not video_id:
            return None

        video_url = f'https://www.youtube.com/watch?v={video_id}'
        logging_info.info(f'File uploaded: {video_url}')

        if notify:
            match = re.search(r'\d{2}-\d{2}-\d{4}', title)
            date = match.group() if match else None
            payload = {
                "success": True,
                "result": {
                    "name": title,
                    "link": video_url,
                    "date": date,
                }
            }
            self._send_notification(payload)

        if remove_file:
            if os.path.exists(video_path):
                os.remove(video_path)

        return video_url

    def modify_title(self, title):
        return title.replace(">", "").replace("<", "")

    def upload_video(self, options: dict):
        """
        Options is Dict with

        file - filepath to video
        title - title of video
        privacyStatus

        :param options:
        :return:
        """
        body = self._generate_meta_data(options)
        connector = self.client.get_authenticated_service()
        insert_request = connector.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(options.get('file'), chunksize=-1, resumable=True)
        )
        try:
            return self._real_upload_video(insert_request)
        except Exception as e:
            logging_info.error(str(e))
            return None

    def _generate_meta_data(self, options: dict):
        return dict(
            snippet=dict(
                title=options.get('title'),
            ),
            status=dict(
                privacyStatus=options.get('privacyStatus'),
            )
        )

    def _real_upload_video(self, insert_request):
        response = None
        error = None
        retry = 0
        logging_info.info('File upload in progress...')
        while response is None:
            try:
                status, response = insert_request.next_chunk()
                logging_info.info('.')
                if 'id' in response:
                    logging_info.info('')
                    return response['id']
            except HttpError as err:
                if err.resp.status in RETRIABLE_STATUS_CODES:
                    error = True
                else:
                    raise
            except RETRIABLE_EXCEPTIONS:
                error = True

            if error:
                retry += 1
                if retry > MAX_RETRIES:
                    raise Exception('Maximum retry are fail')

                sleep_seconds = random.random() * 2 ** retry
                time.sleep(sleep_seconds)

    def _send_notification(self, payload):
        name = payload['result']['name']
        link = payload['result']['link']
        date = payload['result']['date']
        return name, link, date
