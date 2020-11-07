from os import environ
from flask import Flask, request
import requests

app = Flask(__name__)

def build_profile_response(spotify_response):
    json = spotify_response.json()
    response = {
        "display_name": json['display_name'],
        "external_urls": json['external_urls'],
        "images": json['images']
    }

    return response

@app.route("/health")
def health():
    return "I'm healthy!"

@app.route("/profile", methods=['POST'])
def profile():
    token = request.get_json()['token']
    r = requests.get('https://api.spotify.com/v1/me', headers={"Authorization": "Bearer " + token})

    return build_profile_response(r)