import time
import collections
import itertools

from youtube_livechat_messages.models import LiveChatEvent, EventType


class LiveChatEventCursor:

    def __init__(self, request):
        self.request = request

    def events(self, include=None):
        return ChatEventIterator(self.request, include)

    def text_messages(self):
        return ChatEventIterator(self.request, include=[EventType.textMessageEvent])

    def super_chats(self):
        return ChatEventIterator(self.request, include=[EventType.superChatEvent])

    def fan_fundings(self):
        return ChatEventIterator(self.request, include=[EventType.fanFundingEvent])

    def raw(self):
        return RawChatEventCursor(request=self.request)


class RawChatEventCursor:

    def __init__(self, request):
        self.request = request

    def events(self, include=None):
        return RawEventIterator(self.request, include)

    def text_messages(self):
        return RawEventIterator(self.request, include=[EventType.textMessageEvent])

    def super_chats(self):
        return RawEventIterator(self.request, include=[EventType.superChatEvent])

    def fan_fundings(self):
        return RawEventIterator(self.request, include=[EventType.fanFundingEvent])


class ChatEventIterator:

    def __init__(self, request, include=None):
        self.request = request
        self.index = None
        self._events = collections.OrderedDict()
        self.include = include or []

        self.update_events()

        if self._events:
            self.index = list(self._events.keys())[0]

    def update_events(self):
        res = self.request.call()

        for item in res.json()['items']:
            item = LiveChatEvent(item)
            self._events[item.id] = item

    def wait_while_index_set(self):
        """最初の１コメント目を待つ"""
        while True:
            if self.index is None:
                if self._events:
                    self.index = list(self._events.keys())[0]
                    return
                else:
                    self.update_events()
                    time.sleep(1)
            else:
                return

    def wait_for_next_item(self):
        while True:
            item_iter = itertools.dropwhile(lambda item_id: item_id != self.index, self._events)

            next(item_iter)
            try:
                self.index = next(item_iter)
                item = self._events[self.index]
                if not self.include or item.type in self.include:
                    return item
            except StopIteration:
                time.sleep(1)
                self.update_events()

    def __next__(self) -> LiveChatEvent:
        if not self._events:
            time.sleep(1)
            self.update_events()

        self.wait_while_index_set()

        item = self.wait_for_next_item()
        return item

    def __iter__(self):
        return self


class RawEventIterator(ChatEventIterator):

    def __init__(self, request, include=None):
        super().__init__(request, include=include)

    def __next__(self) -> object:
        item = super().__next__()
        return item.raw_json
