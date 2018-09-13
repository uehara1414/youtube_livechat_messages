from youtube_livechat_messages.cursor import LiveChatMessageCursor

import requests


class API:

    def __init__(self, access_token):
        self.access_token = access_token
        self._cursor = None

    def cursor(self, live_chat_id=None, video_id=None, raw=False):
        if not live_chat_id and not video_id:
            raise RuntimeError()
        if video_id:
            raise NotImplementedError()
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
            # fixme: raise Error
            return 'not found.'

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
        return requests.get(self.url, params=self.params, headers=self.headers)
