
from models import Item

import simpledb as db


class ItemController(object):

    def __init__(self, db=db):
        self.db = db.SimpleDB()

    def add(self, url, token):
        item = Item(url, token, self.db)
        item.save(fields=["url", "token", "failed_count", "is_active"])

    def get_active_items(self):
        results = self.db.query("is_active", "YES")
        items = []
        for result in results["Items"]:
            item = Item(
                is_existing=True,
                id_=result["Name"],
                url=self.get_attribute("url", result["Attributes"]),
                token=self.get_attribute("token", result["Attributes"]),
                failed_count=int(
                    self.get_attribute("failed_count", result["Attributes"])
                ),
                db=self.db,
            )
            items.append(item)
        return items

    @staticmethod
    def get_attribute(attribute_name, attributes):
        for attribute in attributes:
            if attribute["Name"] == attribute_name:
                return attribute["Value"]
