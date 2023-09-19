import time

from datetime import datetime
from datetime import timedelta

import jwt
import requests


def make_http_headers(access_token: str) -> dict:
    return {
        "authorization": f"Bearer {access_token}",
        "content-type": "application/json"
    }


def generate_access_token(
        account_id: str,
        authorization_token: str
) -> str:

    GRANT_TYPE = 'account_credentials'
    url = f"https://zoom.us/oauth/token?grant_type={GRANT_TYPE}&account_id={account_id}"
    headers = {
        'Authorization': f'Bearer {authorization_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers)
        response.raise_for_status()
        return response.json()['access_token']
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {str(e)}')
        raise


def make_jwt_payload(client_id: str, token_exp_delta: int) -> dict:
    dt = datetime.utcnow() + timedelta(seconds=token_exp_delta)
    exp = int(time.mktime(dt.timetuple()))

    return {
        "iss": client_id,
        "exp": exp
    }


def generate_jwt_token(payload: dict, client_secret: str) -> str:
    encoded = jwt.encode(payload, client_secret, algorithm='HS256')
    if isinstance(encoded, bytes):
        # For PyJWT <= 1.7.1
        return encoded.decode()
    # For PyJWT >= 2.0.0a1
    return encoded

