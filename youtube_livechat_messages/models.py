from youtube_livechat_messages.utils import isostr_to_datetime


class EventType:
    # Todo: Support more events
    textMessageEvent = "textMessageEvent"
    superChatEvent = "superChatEvent"
    fanFundingEvent = "fanFundingEvent"


class Author:

    def __init__(self, author_json):
        self.raw_json = author_json

        self.channel_id = self.raw_json['channelId']
        self.channel_url = self.raw_json['channel_url']
        self.display_name = self.raw_json['display_name']
        self.profile_image_url = self.raw_json['profile_image_url']
        self.is_verified = self.raw_json['isVerified']
        self.is_chat_owner = self.raw_json['isChatOwner']
        self.is_chat_sponsor = self.raw_json['isChatSponsor']
        self.is_chat_moderator = self.raw_json['isChatModerator']


class LiveChatItem:

    def __init__(self, item_json):
        self.raw_json = item_json

        self.id = self.raw_json['id']
        self.published_at = isostr_to_datetime(self.raw_json['snippet']['publishedAt'])
        self.author = Author(self.raw_json['authorDetails'])

        self.type = self.raw_json['snippet']['type']
        self.has_display_content = self.raw_json['snippet']['hasDisplayContent']

    @property
    def details(self):
        if self.type == EventType.textMessageEvent:
            return self.raw_json['snippet']['textMessageDetails']
        elif self.type == EventType.superChatEvent:
            return self.raw_json['snippet']['superChatDetails']
        elif self.type == EventType.fanFundingEvent:
            return self.raw_json['snippet']['fanFundingEvent']
        return {
            'Error': 'Unsupported EventType.'
        }

    @property
    def display_message(self):
        if self.has_display_content:
            return self.raw_json['snippet']['displayMessage']
        else:
            return ''

    def __lt__(self, other):
        return self.published_at < other.published_at

    def __str__(self):
        return f'LiveChatItem({self.type}: "{self.display_message}")'
