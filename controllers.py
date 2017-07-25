
from models import Item

import simpledb as db


class ItemController(object):

    def __init__(self, db=db):
        self.db = db.SimpleDB()

    def add(self, url, token):
        item = Item(url, token, self.db)
        item.save(fields=["url", "token", "failed_count", "is_active"])

    def get_active_items(self):
        return self.db.query("is_active", "YES")
