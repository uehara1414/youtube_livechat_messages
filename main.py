import os
from youtube_livechat_messages import get_credentials, API, EventType

# OAuth2 authentication
credentials = get_credentials(client_secret_path='client_secret.json')

api = API(credentials=credentials)  # or api = API(access_token)

# get live chat messages from video_id, channel_id or live_chat_id
for message in api.cursor(live_chat_id=os.getenv('LIVE_CHAT_ID')).text_messages():
    print(message.author.display_name, message.display_message)
    # uehara1414 カツ丼食べたい
    # ...

# get super_chats
for super_chat in api.cursor(video_id=os.getenv('VIDEO_ID')).super_chats():
    print(super_chat.author.display_name, super_chat.user_comment, super_chat.amount_display_string)
    # uehara1414 実装お疲れ様です ¥200
    # ...

# get fan_fundings
for super_chat in api.cursor(channel_id=os.getenv('CHANNEL_ID')).fun_fundings():
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
