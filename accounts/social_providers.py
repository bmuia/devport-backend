import urllib.parse
import requests
from django.conf import settings

google_client_id = settings.GOOGLE_CLIENT_ID
google_client_secret = settings.GOOGLE_CLIENT_SECRET    
redirect_uri = settings.REDIRECT_URI


def get_google_auth_url():
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"

    params = {
        'client_id': google_client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'consent'
    }

    return f"{base_url}?{urllib.parse.urlencode(params)}"


def get_google_tokens(code):
    token_url = "https://oauth2.googleapis.com/token"

    token_data = {
        'client_id': google_client_id,
        'client_secret': google_client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, data=token_data)
    return response.json()


def get_google_user_info(access_token):
    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers=headers
    )

    return user_info_response.json()
