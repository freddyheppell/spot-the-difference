
from os import environ

USERS_TABLE = environ.get('USERS_TABLE')

def persist_user(client, share_code, access_token, refresh_token, expiry_time, user_id):
    return client.put_item(
        TableName=USERS_TABLE,
        Item= {
            "share_code": {'S': share_code},
            "access_token": {'S': access_token},
            "refresh_token": {'S': refresh_token},
            "expiry_time": {'N': str(expiry_time)},
            "user_id": {'S': user_id},
        }
    )

def update_user(client, share_code, access_token, refresh_token, expiry_time):
    return client.update_item(
        TableName=USERS_TABLE,
        Key={
            "share_code": {'S': share_code}
        },
        UpdateExpression="set access_token=:access_token, refresh_token=:refresh_token, expiry_time=:expiry_time",
        ExpressionAttributeValues= {
            ":access_token": {'S': access_token},
            ":refresh_token": {'S': refresh_token},
            ":expiry_time": {'N':str(expiry_time)}
        }
    )


def result_to_user(result):
    return {
        "access_token": result.get("access_token").get("S"),
        "expiry_time": result.get("expiry_time").get("N"),
        "refresh_token": result.get("refresh_token").get("S"),
        "share_code": result.get("share_code").get("S"),
        "user_id": result.get("user_id").get("S")
    }

def get_user_by_share_code(client, share_code):
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'share_code': { 'S': share_code }
        }
    )

    item = resp.get("Item")

    return result_to_user(item)

