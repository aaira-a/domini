
from models import Item

import simpledb as db


class ItemController(object):

    @staticmethod
    def add(url, token):
        item = Item(url, token)
        item.save(fields=["url", "token", "failed_count", "is_active"])

    @staticmethod
    def get_active_items():
        db_instance = db.SimpleDB()
        return db_instance.query("is_active", "YES")
