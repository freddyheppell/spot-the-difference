import requests
from os import environ
from base64 import b64encode
import time

from requests_futures.sessions import FuturesSession

from flask import jsonify

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



def exchange_code(redirect_uri,code):
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

def refresh(user):
    if int(user["expiry_time"]) > int(time.time()):
        return user
    else:
        body = {
            "grant_type": "refresh_token",
            "refresh_token": user["refresh_token"]
        } 

        headers = {
            "Authorization": basic_encoded()
        }

        resp = requests.post('https://accounts.spotify.com/api/token', data=body, headers=headers)

        if resp.status_code != 200:
            raise Exception(resp.json())

        return resp.json()

def response_hook(resp, *args, **kwargs):
    resp.data = resp.json()

def user_top_for(session, token, type, time):
    print("make a request")
    params = {
        "time_range": time,
        "limit": 50,
        "offset": 0
    }
    
    return session.get("https://api.spotify.com/v1/me/top/" + type, params=params,
    headers={"Authorization": "Bearer " + token},
    hooks={
        'response': response_hook,
    })

def get_user_top(session, token):
    return {
        "long_term": {
            "artists": user_top_for(session, token,  "artists", "long_term"),
            "tracks": user_top_for(session,token, "tracks", "long_term"),
        },
        "medium_term": {
            "artists": user_top_for(session,token, "artists", "medium_term"),
            "tracks": user_top_for(session,token, "tracks", "medium_term"),
        },
        "short_term": {
            "artists": user_top_for(session,token, "artists", "short_term"),
            "tracks": user_top_for(session, token,"tracks", "short_term"),
        }
    }

def async_user_from_token(session, token):
    return session.get('https://api.spotify.com/v1/me',
        headers={"Authorization": "Bearer " + token},
        hooks={
            'response': response_hook,
        }
    )

blacklist = set([
    "followers",
    "href",
    "type",
    "uri",
    "album",
    "available_markets",
    "disc_number",
    "duration_ms",
    "explicit",
    "external_ids",
    "is_local",
    "preview_url",
    "track_number"
])

def filter_popular_item(item):
    new_data = {}
    for k, v in item.items():
        if k not in blacklist:
            new_data[k] = v

    return new_data

def filter_popular_response(data):
    items = data["items"]

    return list(map(filter_popular_item, items))