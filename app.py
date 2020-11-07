from os import environ
from flask import Flask, request
import requests
import spotify
import boto3
import share_code

app = Flask(__name__)

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
    passthrough_share_code = json["share_code"] if "share_code" in json else None

    data = {
        "access_token": json["access_token"],
        "expires_in": json["expires_in"],
        "refresh_token": json["refresh_token"]
    }

    # Get the user's ID
    user_id = spotify.get_user_from_token(data["access_token"])["id"]
    data["user_id"] = user_id

    # Make a share code for this user
    data["share_code"] = share_code.generate_share_code(word_list)

    # Persist to db
    resp = client.put_item(
        TableName=USERS_TABLE,
        Item= {
            "share_code": {'S': data["share_code"]},
            "access_token": {'S': data["access_token"]},
            "refresh_token": {'S': data["refresh_token"]},
            "expires_in": {'S': data["expires_in"]},
        }
    )

    return {
        "share_codes": [data["share_code"], passthrough_share_code]
    }