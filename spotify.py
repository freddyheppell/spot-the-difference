import requests
from os import environ
from base64 import b64encode

def sanitise_profile_response(spotify_response):
    response = {
        "id": spotify_response['id'],
        "display_name": spotify_response['display_name'],
        "external_urls": spotify_response['external_urls'],
        "images": spotify_response['images']
    }

    return response

def get_user_from_token(token):
    resp = requests.get('https://api.spotify.com/v1/me', headers={"Authorization": "Bearer " + token})

    if resp.status_code != 200:
        raise Exception(resp.json())

    return resp.json()

def exchange_code(code):
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": environ.get('REDIRECT_URI')
    }

    headers = {
        "Authorization": basic_encoded()
    }

    resp = requests.post('https://accounts.spotify.com/api/token', data=body, headers=headers)

    if resp.status_code != 200:
        raise Exception(resp.json())

    return resp.json()

def basic_encoded():
    key_string = environ.get('CLIENT_ID')+ ":" + environ.get('CLIENT_SECRET')
    key_string_encoded = key_string.encode('ascii')
    key_string_b64 = b64encode(key_string_encoded)

    return "Basic " +  key_string_b64.decode('ascii')