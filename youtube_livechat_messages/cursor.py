import time
import collections
import itertools

from youtube_livechat_messages.models import LiveChatEvent, EventType


class LiveChatEventCursor:

    def __init__(self, request, raw=False, include=None):
        self.request = request
        self.raw = raw
        self.index = None
        self._items = collections.OrderedDict()
        self.include = include or []

        self.update_events()

        if self._items:
            self.index = list(self._items.keys())[0]

    def update_events(self):
        res = self.request.call()

        for item in res.json()['items']:
            item = LiveChatEvent(item)
            self._items[item.id] = item

    def wait_while_index_set(self):
        """最初の１コメント目を待つ"""
        while True:
            if self.index is None:
                if self._items:
                    self.index = list(self._items.keys())[0]
                    return
                else:
                    self.update_events()
                    time.sleep(1)
            else:
                return

    def __iter__(self):
        return self

    def wait_for_next_item(self):
        while True:
            item_iter = itertools.dropwhile(lambda item_id: item_id != self.index, self._items)

            next(item_iter)
            try:
                self.index = next(item_iter)
                item = self._items[self.index]
                if not self.include or item.type in self.include:
                    return item
            except StopIteration:
                time.sleep(1)
                self.update_events()

    def __next__(self):
        if not self._items:
            time.sleep(1)
            self.update_events()

        self.wait_while_index_set()

        item = self.wait_for_next_item()
        if self.raw:
            return item.raw
        else:
            return item

    def events(self, include=None):
        self.include = include or []
        return self

    def super_chats(self):
        self.include = [EventType.superChatEvent]
        return self

    def text_messages(self):
        self.include = [EventType.textMessageEvent]
        return self

    def fun_fundings(self):
        self.include = [EventType.fanFundingEvent]
        return self
