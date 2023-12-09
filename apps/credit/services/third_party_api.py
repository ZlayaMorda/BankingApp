import requests
import json


class CreditAPI:
    api_url = "https://api.nbrb.by/refinancingrate"

    def get_last_refinancing_rate(self):
        content = json.loads(requests.get(self.api_url).content)
        return float(content.pop()["Value"])
