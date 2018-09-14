import os

from youtube_livechat_messages import get_access_token, API
from youtube_livechat_messages.auth import get_credentials

access_token = get_access_token()
credentials = get_credentials()

api = API(access_token, credentials)
live_chat_id = api.get_live_chat_id_from_video_id(os.getenv('VIDEO_ID'))


for item in api.cursor(live_chat_id):
    print(item)
