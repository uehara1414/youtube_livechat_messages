from oauth2client import tools
from oauth2client import client
from oauth2client.file import Storage


def get_access_token():
    credentials_path = "credentials.json"
    storage = Storage(credentials_path)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        f = 'client_secret.json'
        scope = "https://www.googleapis.com/auth/youtube.readonly"
        flow = client.flow_from_clientsecrets(f, scope)
        flow.user_agent = "hoge"
        credentials = tools.run_flow(flow, Storage(credentials_path))

    return credentials.access_token
