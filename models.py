import requests


class Item(object):

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def fetch_from_provider(self):
        try:
            headers = {"Authorization": self.token}
            self.latest_call = requests.get(self.url, headers=headers)
        except Exception as e:
            self.latest_call = ("failed: " + str(e))
