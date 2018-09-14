import os

from youtube_livechat_messages import get_access_token, API
from youtube_livechat_messages.auth import get_credentials

access_token = get_access_token()
credentials = get_credentials()

api = API(access_token, credentials)

for item in api.cursor(video_id=os.getenv('VIDEO_ID')):
    print(item)
