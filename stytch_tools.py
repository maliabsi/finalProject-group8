# pylint: disable=protected-access

"""Tools for using stytch with this project"""
import os
import json
from stytch import Client


client = Client(
    project_id=os.getenv("PROJECT_ID"),
    secret=os.getenv("STYTCH_SECRET"),
    environment="test",
)


def stytch_auth(token):
    """
    Authenticates a token with stytch

    returns id if authenticated, otherwise returns None
    """
    response = client.oauth.authenticate(token)

    # If the response is a 200, the user is verified and can be logged in
    # (Copied from Stytch API docs)
    if response.status_code == 200:
        return json.loads(response._content.decode("UTF-8"))["user_id"], True

    return None, None


def get_user_data(stytch_id):
    """
    Returns user data, given a user_id
    Data in format:
    {
        'created_at': '2022-04-05T18:43:15Z',
        'crypto_wallets': [],
        'emails': [
            {
                'email': 'mcfralish@yahoo.com',
                'email_id': 'email-test-7bafd4b3-893e-4bc8-8a31-8a8b41605afc',
                'verified': False
            }
        ],
        'name': {
            'first_name': 'Michael',
            'last_name': 'Fralish',
            'middle_name': ''
        },
        'phone_numbers': [],
        'providers': [
            {
                'provider_subject': '10228086012278278',
                'provider_type': 'Facebook'
            }
        ],
        'request_id': 'request-id-test-87f5b438-3261-4425-9c78-90734afb3103',
        'status': 'active',
        'status_code': 200, 'totps': [],
        'user_id': 'user-test-552d704c-39b0-4c02-a0a1-f9d71a7473d9',
        'webauthn_registrations': []
    }
    """
    user = client.users.get(stytch_id)
    return json.loads(user._content.decode("UTF-8")), True
