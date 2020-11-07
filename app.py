from os import environ
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import spotify
import boto3
import share_code
import user_db
import datetime

app = Flask(__name__)
CORS(app)

IS_OFFLINE = environ.get('IS_OFFLINE')

word_list = share_code.load()

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    client = boto3.client('dynamodb')

@app.route("/health")
def health():
    return "I'm healthy!"


@app.route("/profile", methods=['POST'])
def profile():
    share_code = request.get_json()['share_code']
    print(share_code)
    user = user_db.get_user_by_share_code(client, share_code)

    if not user:
        return {
            "error": "Share code not found"
        }, 404

    # See if the user's API token needs to be refreshed
    try:
        refreshed_keys = spotify.refresh(user)
    except Exception as e:
        return {
            "desc": "Error refreshing API token",
            "error": str(e)
        }, 500

    print(user["expiry_time"])

    if refreshed_keys["access_token"] != user["access_token"]:
        # Key has been refreshed
        user_db.update_user(client, share_code, refreshed_keys["access_token"], refreshed_keys["refresh_token"], refreshed_keys["expiry_time"])

    spotify_profile = spotify.get_user_from_token(refreshed_keys["access_token"])

    return spotify.sanitise_profile_response(spotify_profile)

@app.route("/authorise", methods=["POST"])
def authorise():
    json = request.get_json()
    spotify_code = json["spotify_code"]
    passthrough_share_code = json["share_code"] if "share_code" in json else None

    try:
        access_token = spotify.exchange_code(spotify_code)
    except Exception as e:
        return {
            "desc": "Error exchanging code",
            "error": str(e)
        }, 500

    data = {
        "access_token": access_token["access_token"],
        "expires_in": access_token["expires_in"],
        "refresh_token": access_token["refresh_token"]
    }

    # Get the user's ID
    try:
        user_id = spotify.get_user_from_token(data["access_token"])["id"]
    except Exception as e:
        return {
            "desc": "Error retrieving user",
            "error": str(e)
        }, 500

    user_share_code = share_code.generate_share_code(word_list)

    expiry_time = datetime.datetime.today() + datetime.timedelta(seconds=access_token["expires_in"])

    user_db.persist_user(
        client,
        user_share_code,
        access_token["access_token"],
        access_token["refresh_token"],
        expiry_time.strftime('%s'),
        user_id
    )

    return {
        "share_codes": [user_share_code, passthrough_share_code]
    }

# @app.route("/compare", methods=["POST"])
# def compare():
#     json = request.get_json()
#     share_codes = json["share_codes"]

#     if len(share_codes) != 2:
#         return jsonify({"error": "Must provide 2 codes"}), 422

#     resp = {}

#     for share_code in share_codes:
#         user = user_db.get_user_by_share_code(share_code)
#         display_name, data = spotify.get_music_data_for_token(token)
#         resp[display_name] = data

#     return resp