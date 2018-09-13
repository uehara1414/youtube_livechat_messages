class LiveChatItem:

    def __init__(self, item_json):
        self.raw = item_json

        self.id = item_json['id']
        self.published_at = item_json['snippet']['publishedAt']
        self.display_message = item_json['snippet']['displayMessage']

        self.type = item_json['snippet']['type']
        if self.type == 'textMessageEvent':
            self.details = item_json['snippet']['textMessageDetails']
        elif self.type == 'superChatEvent':
            self.details = item_json['snippet']['superChatDetails']
        elif self.type == 'fanFundingEvent':
            self.details = item_json['snippet']['fanFundingEvent']
        else:
            self.details = None

    def __lt__(self, other):
        return self.published_at < other.published_at

    def __str__(self):
        return f'{self.id[:5]} {self.type}: {self.display_message} at {self.published_at}'
