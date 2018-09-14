import os

from youtube_livechat_messages import get_credentials, API

credentials = get_credentials()

api = API(credentials=credentials)

for item in api.cursor(video_id=os.getenv('VIDEO_ID')):
    print(item)
