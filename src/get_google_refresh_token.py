# -*- coding: utf-8 -*-

import requests
from celery import shared_task
from core.models import ZoomYouTubeFile, UserCredential


TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
GRANT_TYPE = 'authorization_code'


@shared_task()
def get_token(user: int, code: str, client_id: str, client_secret: str, url=TOKEN_URL, redirect_uri=REDIRECT_URI, grant_type=GRANT_TYPE):
    try:
        assert code, "Not found GOOGLE_CODE"
        assert client_id, "Not found GOOGLE_CLIENT_ID"
        assert client_secret, "Not found GOOGLE_CLIENT_SECRET"

        user_zoom = UserCredential.objects.get(user=user)

        payload = dict(
            code=code,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            grant_type=grant_type
        )
        response = requests.request('POST', url, data=payload)
        if response.status_code != 200:
            error_message = response.json().get('error_description')
            return {
                'error': error_message
            }
        else:
            user_zoom.google_refresh_token = response.json().get('refresh_token')
            user_zoom.save()
    except UserCredential.DoesNotExist:
        print("User not found")
    except Exception as e:
        print(e)
