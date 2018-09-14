# youtube_livechat_messages
[![PyPI Version](https://img.shields.io/pypi/v/youtube_livechat_messages.svg)](https://pypi.python.org/pypi/youtube_livechat_messages)

Youtube LiveChatMessages list API wrapper.

## Requirements
- YouTube Data API v3 client_secret json file

## Installation
```sh
pipenv install youtube_livechat_messages
```

## Quick Start
```python
import os
from youtube_livechat_messages import get_credentials, API, EventType

# OAuth2 authentication
credentials = get_credentials(client_secret_path='client_secret.json')

api = API(credentials=credentials)  # or api = API(access_token)

# get live chat messages from video_id, channel_id or live_chat_id
for message in api.cursor(video_id=os.getenv('VIDEO_ID')).text_messages():
    print(message.author.display_name, message.display_message)
    # uehara1414 カツ丼食べたい
    # ...

# get super_chats
for super_chat in api.cursor(live_chat_id=os.getenv('LIVE_CHAT_ID')).super_chats():
    print(super_chat.author.display_name, super_chat.user_comment, super_chat.amount_display_string)
    # uehara1414 実装お疲れ様です ¥200
    # ...

# get fan_fundings
for super_chat in api.cursor(channel_id=os.getenv('CHANNEL_ID')).fan_fundings():
    print(super_chat.author.display_name, super_chat.amount_display_string)
    # uehara1414 ¥200
    # ...

# filter events
for event in api.cursor(video_id=os.getenv('VIDEO_ID')).events(include=[EventType.textMessageEvent, EventType.fanFundingEvent]):
    if event.type == EventType.textMessageEvent:
        print(event.display_message)
        # こんばんは
    elif event.type == EventType.fanFundingEvent:
        print(event.currency)
        # JPY

# get raw event json
for event in api.cursor(video_id=os.getenv('VIDEO_ID')).raw().events():
    print(event['snippet']['type'], event['snippet']['displayMessage'])
    # textMessageEvent Hello World
```

## Features
- OAuth2 authentication
- Messages, Super chats and Fun funding's Real time event loading
- Auto access token refresh

## Models
### LiveChatEvent
- id
- published_at
- author (Author)
- type (EventType(str))
- details (json)
- raw_json (json)
- display_message
- amount_micros (superChat or funFunding only)
- currency (superChat or funFunding only)
- amount_display_string (superChat or funFunding only)
- user_comment (superChat or funFunding only)

### Author
- channel_id
- channel_url
- display_name
- profile_image_url
- is_verified
- is_chat_owner
- is_chat_sponsor
- is_chat_moderator

## Todo
- [ ] 動画終了時の処理
- [ ] 認証部分の依存先からoauth2clientを外す(oauth2client is now deprecated.)
- [ ] テキスト・投げ銭・スーパーチャット以外のイベントへの対応

## Contributing
個人的に必要な状況で十分に使える程度の実装しかしていません。

足りない機能、不具合などたくさん有るかと思うので、バグ報告・要望・修正はIssues, PullRequests か、[uehara1414](https://twitter.com/uehara1414/)までお気軽に。
