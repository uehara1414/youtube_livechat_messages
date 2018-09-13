import os

from youtube_livechat_messages import get_access_token, API

access_token = get_access_token()

api = API(access_token)
live_chat_id = api.get_live_chat_id_from_video_id(os.getenv('LIVE_CHAT_ID'))

for item in api.cursor(live_chat_id):
    print(item)
