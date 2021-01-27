import requests
from os import environ
from base64 import b64encode
import time

from requests_futures.sessions import FuturesSession

from flask import jsonify

# Grab the fields to return to users for a spotify profile response
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

# Exchange an authorization code
# Requires the redirect uri for spotify api reasons
def exchange_code(redirect_uri,code):
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }

    headers = {
        "Authorization": basic_encoded()
    }

    resp = requests.post('https://accounts.spotify.com/api/token', data=body, headers=headers)

    if resp.status_code != 200:
        raise Exception(resp.json())

    return resp.json()

# Generate the basic authorization header
def basic_encoded():
    key_string = environ.get('CLIENT_ID')+ ":" + environ.get('CLIENT_SECRET')
    key_string_encoded = key_string.encode('ascii')
    key_string_b64 = b64encode(key_string_encoded)

    return "Basic " +  key_string_b64.decode('ascii')

# Refresh a user with the spotify api
def refresh(user):
    if int(user["expiry_time"]) > int(time.time()):
        # Don't refresh if the user's token expiry time is in the future
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

# Function to deserialise the response
def response_hook(resp, *args, **kwargs):
    resp.data = resp.json()

# Get the user's top response
# Type: "tracks", "artists"
# Time:"short_term", "medium_term", "long_term"
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

# Fetch all the users' top data
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

# Asynchronously fetch the user, using a given FuturesSession
def async_user_from_token(session, token):
    return session.get('https://api.spotify.com/v1/me',
        headers={"Authorization": "Bearer " + token},
        hooks={
            'response': response_hook,
        }
    )

# Terms to remove from top responses
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

# Filter a single popular item against the blacklist
def filter_popular_item(item):
    new_data = {}
    for k, v in item.items():
        if k not in blacklist:
            new_data[k] = v

    return new_data

# Filter a set of popular items against the blacklist
def filter_popular_response(data):
    items = data["items"]

    return list(map(filter_popular_item, items))