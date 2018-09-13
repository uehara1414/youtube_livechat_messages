import time
import collections
import itertools

from youtube_livechat_messages.models import LiveChatItem


class LiveChatMessageCursor:

    def __init__(self, request, raw=False):
        self.request = request
        self.raw = raw
        self.index = None
        self._items = collections.OrderedDict()

        self.update_comments()

        if self._items:
            self.index = list(self._items.keys())[0]

    def update_comments(self):
        res = self.request.call()

        for item in res.json()['items']:
            item = LiveChatItem(item)
            self._items[item.id] = item

        print('.')

    def wait_while_index_set(self):
        while True:
            if self.index is None:
                if self._items:
                    self.index = list(self._items.keys())[0]
                    return
                else:
                    self.update_comments()
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
                return item
            except StopIteration:
                time.sleep(1)
                self.update_comments()

    def __next__(self):
        if not self._items:
            time.sleep(1)
            self.update_comments()

        self.wait_while_index_set()

        item = self.wait_for_next_item()
        if self.raw:
            return item.raw
        else:
            return item
