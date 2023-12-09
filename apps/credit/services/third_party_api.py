import requests
import json

from utils.exceptions import NotFound


class CreditAPI:
    api_url = "https://api.nbrb.by/refinancingrate"

    def get_last_refinancing_rate(self):
        try:
            content = json.loads(requests.get(self.api_url).content)
            return float(content.pop()["Value"])
        except Exception:
            raise NotFound("Can't get rate")
