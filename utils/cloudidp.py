import os
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient

def get_oauth2_config():
    client_cert = os.environ.get("CLIENT_CERTIFICATE")
    client_key = os.environ.get("CLIENT_PRIVATE_KEY")

    return {
        'client_id': os.environ.get("CIDP_CLIENT_ID"),
        'client_secret': os.environ.get("CIDP_CLIENT_SECRET"),
        'token_url': os.environ.get("CIDP_TOKEN_URL"),
    }, (client_cert, client_key)

def setEnvironment():
    config, (cert, key)= get_oauth2_config()
    
    oauth = OAuth2Session(
        client=LegacyApplicationClient(client_id=config['client_id']),
        scope=['email', 'profile'],
    )

    try:
        token = oauth.fetch_token(
            token_url=config['token_url'],
            username='',
            password='',
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            cert=(cert, key),
            timeout=5,
        )
        print(f"Token: {token['access_token'][:10]}")
        os.environ["service__catalog_CIDP_TOKEN"] = token['access_token']
    except Exception as e:
        print(f"Token request failed: {e}")
