from os import environ
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import spotify
import boto3
import share_code

app = Flask(__name__)
CORS(app)

USERS_TABLE = environ.get('USERS_TABLE')
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
    token = request.get_json()['token']
    response = spotify.get_user_from_token(token)

    return spotify.sanitise_profile_response(response)

@app.route("/authorise", methods=["POST"])
def authorise():
    json = request.get_json()
    spotify_code = json["spotify_code"]
    passthrough_share_code = json["share_code"] if "share_code" in json else None

    access_token = spotify.exchange_code(spotify_code)

    data = {
        "access_token": access_token["access_token"],
        "expires_in": access_token["expires_in"],
        "refresh_token": access_token["refresh_token"]
    }

    # Get the user's ID
    user_id = spotify.get_user_from_token(data["access_token"])["id"]

    # Persist to db
    resp = client.put_item(
        TableName=USERS_TABLE,
        Item= {
            "share_code": {'S': share_code.generate_share_code(word_list)},
            "access_token": {'S': access_token["access_token"]},
            "refresh_token": {'S': access_token["refresh_token"]},
            "expires_in": {'S': access_token["expires_in"]},
            "user_id": {'S': user_id},
        }
    )

    return {
        "share_codes": [data["share_code"], passthrough_share_code]
    }

# @app.route("/compare", methods=["POST"])
# def compare():
#     json = request.get_json()
#     share_codes = json["share_codes"]

#     if len(share_codes) != 2:
#         return jsonify({"error": "Must provide 2 codes"}), 422

#     resp = {}

#     for share_code in share_codes:
        