import requests

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