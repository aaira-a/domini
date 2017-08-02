
from models import Item

import messaging
import simpledb as db


class ItemController(object):

    def __init__(self, db=db, messenger=messaging):
        self.db = db.SimpleDB()
        self.db.create_domain()
        self.messenger = messenger.TwilioClient()

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
                phone=self.get_attribute("phone", result["Attributes"]),
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

    def process_items(self, items):
        try:
            for item in items:
                status = item.fetch_status_from_provider()
                if "error" in status:
                    item.increment_failed_count()
                elif "DL" in status:
                    self.messenger.send_message(
                        "your item is out for delivery now", item.phone)
        except Exception:
            pass
