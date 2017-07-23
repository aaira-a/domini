
from models import Item


class ItemController(object):

    @staticmethod
    def add(url, token):
        item = Item(url, token)
        item.save(fields=["url", "token", "failed_count", "is_active"])
