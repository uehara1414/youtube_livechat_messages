from youtube_livechat_messages.cursor import LiveChatEventCursor
from youtube_livechat_messages.auth import auto_refresh

import requests


class API:

    def __init__(self, access_token=None, credentials=None):
        if not access_token and not credentials:
            raise RuntimeError('You should set access_token or credentials')
        if credentials:
            self.access_token = credentials.access_token
            self.expired_at = credentials.token_expiry
            self.client_id = credentials.client_id
            self.client_secret = credentials.client_secret
            self.refresh_token = credentials.refresh_token
        else:
            self.access_token = access_token
            self.expired_at = None
            self.client_id = None
            self.client_secret = None
            self.refresh_token = None
        self.credentials = credentials

    @property
    def refreshable(self):
        return self.credentials is not None

    def cursor(self, live_chat_id=None, video_id=None, channel_id=None):
        if not live_chat_id and not video_id and not channel_id:
            raise RuntimeError('You should set live_chat_id, video_id or channel_id')
        live_chat_id = live_chat_id or self.get_live_chat_id(video_id=video_id, channel_id=channel_id)
        api_request = APIRequest(self, params={'part': 'snippet,authorDetails,id', 'liveChatId': live_chat_id})

        return LiveChatEventCursor(api_request)

    def get_live_chat_id(self, video_id=None, channel_id=None):
        if not video_id and not channel_id:
            raise RuntimeError('')
        live_chat_id = None
        if channel_id:
            video_id = self.get_video_id_from_channel_id(channel_id)
        if video_id:
            live_chat_id = self.get_live_chat_id_from_video_id(video_id)
        return live_chat_id

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
            raise RuntimeError('The LiveBroadcast Not Found.')

    def get_live_chat_id_from_video_id(self, video_id):
        request = APIRequest(self, "https://www.googleapis.com/youtube/v3/videos", params={
            'part': 'snippet,contentDetails,statistics,liveStreamingDetails',
            'id': video_id
        })
        res = request.call()

        try:
            return res.json()['items'][0]['liveStreamingDetails']['activeLiveChatId']
        except (IndexError, KeyError):
            raise RuntimeError('The LiveChat Not Found.')


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
        if self.api.refreshable:
            self.api.access_token, self.api.expired_at = auto_refresh(self.api.access_token,
                                                                      self.api.client_id,
                                                                      self.api.client_secret,
                                                                      self.api.refresh_token,
                                                                      self.api.expired_at)

        res = requests.get(self.url, params=self.params, headers=self.headers)

        if not res.ok:
            raise RuntimeError(res.text)
        return res
