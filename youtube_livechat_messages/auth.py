from datetime import datetime, timedelta

from oauth2client import tools
from oauth2client import client
from oauth2client.file import Storage
import requests


def get_access_token():
    return get_credentials().access_token


def get_credentials():
    credentials_path = "credentials.json"
    storage = Storage(credentials_path)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        f = 'client_secret.json'
        scope = "https://www.googleapis.com/auth/youtube.readonly"
        flow = client.flow_from_clientsecrets(f, scope)
        flow.user_agent = "hoge"
        credentials = tools.run_flow(flow, Storage(credentials_path))

    return credentials


def auto_refresh(access_token, client_id, client_secret, refresh_token, expired_at):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }

    if expired_at < datetime.now() - timedelta(minutes=1):
        res = requests.post('https://www.googleapis.com/oauth2/v3/token', data=data)
        r = res.json()
        expired_at = datetime.now() + timedelta(seconds=r['expires_in'])
        access_token = r['access_token']

    return access_token, expired_at
