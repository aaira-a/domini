import requests


class Item(object):

    def __init__(self, url, token, is_existing=False, failed_count=0):
        self.url = url
        self.token = token
        self.failed_count = failed_count

        if not is_existing:
            self.is_active = True
            self.failed_count = 0

    def fetch_from_provider(self):
        try:
            headers = {"Authorization": self.token}
            self.latest_call = requests.get(self.url, headers=headers)
        except Exception as e:
            self.latest_call = ("failed: " + str(e))
            self.failed_count += 1
