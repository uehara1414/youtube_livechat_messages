from youtube_livechat_messages.cursor import LiveChatMessageCursor
from youtube_livechat_messages.auth import auto_refresh

import requests


class API:

    def __init__(self, access_token, credentials=None):
        self.access_token = access_token
        self._cursor = None
        if credentials:
            self.expired_at = credentials.token_expiry
            self.client_id = credentials.client_id
            self.client_secret = credentials.client_secret
            self.refresh_token = credentials.refresh_token
        else:
            self.expired_at = None
            self.client_id = None
            self.client_secret = None
            self.refresh_token = None
        self.credentials = credentials

    def cursor(self, live_chat_id=None, video_id=None, channel_id=None, raw=False):
        if not live_chat_id and not video_id and not channel_id:
            raise RuntimeError()
        if channel_id:
            video_id = self.get_video_id_from_channel_id(channel_id)
        if video_id:
            live_chat_id = self.get_live_chat_id_from_video_id(video_id)

        api_request = APIRequest(self, params={'part': 'snippet,authorDetails,id', 'liveChatId': live_chat_id})

        return LiveChatMessageCursor(api_request, raw=raw)

    def get_video_id_from_channel_id(self, channel_id):
        request = APIRequest(self, "https://www.googleapis.com/youtube/v3/search", params={
            'part': 'snippet',
            'channelId': channel_id
        })
        res = request.call()
        for item in res.json()['items']:
            if item['snippet']['liveBroadcastContent'] == 'live':
                return item['id']['videoId']
        else:
            raise RuntimeError('LiveBroadcast Not Found.')

    def get_live_chat_id_from_video_id(self, video_id):
        request = APIRequest(self, "https://www.googleapis.com/youtube/v3/videos", params={
            'part': 'snippet,contentDetails,statistics,liveStreamingDetails',
            'id': video_id
        })
        res = request.call()

        return res.json()['items'][0]['liveStreamingDetails']['activeLiveChatId']


class APIRequest:

    def __init__(self, api: API, url=None, params=None):
        self.api = api
        self.url = url or 'https://www.googleapis.com/youtube/v3/liveChat/messages'
        self.params = params or {}

    @property
    def headers(self):
        return {
            'Authorization': f'Bearer {self.api.access_token}'
        }

    def call(self):
        self.api.access_token, self.api.expired_at = auto_refresh(self.api.access_token,
                                                                  self.api.client_id,
                                                                  self.api.client_secret,
                                                                  self.api.refresh_token,
                                                                  self.api.expired_at)
        res = requests.get(self.url, params=self.params, headers=self.headers)
        if not res.ok:
            raise RuntimeError()
        return res
