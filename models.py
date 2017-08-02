import uuid

import requests


class Item(object):

    def __init__(self, url, token, phone, db,
                 is_existing=False, failed_count=0, id_=None):
        self.url = url
        self.token = token
        self.phone = phone
        self.failed_count = failed_count
        self.id = id_
        self.db = db

        if not is_existing:
            self.is_active = "YES"
            self.failed_count = 0
            self.id = str(uuid.uuid4())

    def fetch_status_from_provider(self):
        try:
            headers = {"Authorization": self.token}
            response = requests.get(self.url, headers=headers)
            return response.json()["Status"]
        except Exception as e:
            return "error"

    def save(self, fields):
        attributes = []
        for field in fields:
            attributes.append(
                {"Name": field, "Value": str(getattr(self, field))})

        self.db.put_attributes(
            item_name=self.id,
            attributes=attributes,
        )

    def increment_failed_count(self):
        self.failed_count += 1
