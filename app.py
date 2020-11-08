from concurrent.futures.thread import ThreadPoolExecutor
from os import environ
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from requests_futures.sessions import FuturesSession
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

def get_expiry_time(expires_in):
    return (datetime.datetime.today() + datetime.timedelta(seconds=expires_in)).strftime('%s')

def refresh(user):
    # See if the user's API token needs to be refreshed
    try:
        refreshed_keys = spotify.refresh(user)
    except Exception as e:
        return {
            "desc": "Error refreshing API token",
            "error": str(e)
        }, 500

    if refreshed_keys["access_token"] != user["access_token"]:
        # Key has been refreshed
        user_db.update_user(
            client,
            share_code,
            refreshed_keys["access_token"],
            refreshed_keys["refresh_token"] if "refresh_token" in refreshed_keys else user["refresh_token"],
            get_expiry_time(refreshed_keys["expires_in"])
        )

    return refreshed_keys

@app.route("/health")
def health():
    return "I'm healthy!"


@app.route("/profile", methods=['POST'])
def profile():
    share_code = request.get_json()['share_code']
    user = user_db.get_user_by_share_code(client, share_code)

    if not user:
        return {
            "error": "Share code not found"
        }, 404

    refreshed_keys = refresh(user)

    spotify_profile = spotify.get_user_from_token(refreshed_keys["access_token"])

    return spotify.sanitise_profile_response(spotify_profile)

@app.route("/authorise", methods=["POST"])
def authorise():
    json = request.get_json()
    spotify_code = json["spotify_code"]
    passthrough_share_code = json["share_code"] if "share_code" in json else None

    redirect_uri = "https://spotdiff.online" if request.headers.get("Referer").startswith("https://spotdiff.online") else "http://localhost:8080"

    try:
        access_token = spotify.exchange_code(redirect_uri, spotify_code)
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

    expiry_time = get_expiry_time(access_token["expires_in"])

    user_db.persist_user(
        client,
        user_share_code,
        access_token["access_token"],
        access_token["refresh_token"],
        expiry_time,
        user_id
    )

    return {
        "share_codes": [user_share_code, passthrough_share_code]
    }

def defuture(results):
    for term, term_data in results.items():
        for type, type_data in term_data.items():
            results[term][type] = spotify.filter_popular_response(type_data.result().data)

    return results

@app.route("/compare", methods=["POST"])
def compare():
    json = request.get_json()
    share_code_1, share_code_2 = json["share_code_1"], json["share_code_2"]

    user_1 = user_db.get_user_by_share_code(client, share_code_1)
    user_2 = user_db.get_user_by_share_code(client, share_code_2)

    if not user_1 or not user_2:
        return {
            "error": "Share code not found"
        }, 404

    user_1_keys = refresh(user_1)
    user_2_keys = refresh(user_2)

    executor = ThreadPoolExecutor()
    session = FuturesSession(executor)

    user_1_results = spotify.get_user_top(session, user_1_keys["access_token"])
    user_2_results = spotify.get_user_top(session, user_2_keys["access_token"])

    user_1_profile = spotify.async_user_from_token(session, user_1_keys["access_token"])
    user_2_profile = spotify.async_user_from_token(session, user_2_keys["access_token"])

    executor.shutdown(wait=True)

    return {
        "data": [
            {
                "profile": spotify.sanitise_profile_response(user_1_profile.result().data),
                "listening_data": defuture(user_1_results)
            },
            {
                "profile": spotify.sanitise_profile_response(user_2_profile.result().data),
                "listening_data": defuture(user_2_results)
            }
        ]
    }