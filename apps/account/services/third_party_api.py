import decimal

import requests
import json

from utils.exceptions import NotFound


class ExchangeRateAPI:
    api_url = "https://api.nbrb.by/exrates/rates?periodicity=0"
    coef = decimal.Decimal(1.05)

    def get_today_rates(self):
        try:
            usd = 0.
            eur = 0.
            content = json.loads(requests.get(self.api_url).content)
            for i in content:
                if i["Cur_Abbreviation"] == "USD":
                    usd = i["Cur_OfficialRate"]
                elif i["Cur_Abbreviation"] == "EUR":
                    eur = i["Cur_OfficialRate"]
            if usd == 0.0 or eur == 0.0:
                raise NotFound("Can't get rate")
            return {"USD": decimal.Decimal(usd), "EUR": decimal.Decimal(eur)}
        except Exception:
            raise NotFound("Can't get rate")

    def calculate_amount(self, currency_sell, currency_buy, amount):
        if currency_sell == currency_buy:
            return amount
        elif currency_sell == "BYN":
            return round(amount / (self.get_today_rates()[currency_buy] * self.coef), 2)
        else:
            if currency_buy == "BYN":
                return round(amount * (self.get_today_rates()[currency_sell]), 2)
            else:
                in_byn = round(amount * (self.get_today_rates()[currency_sell]), 2)
                return self.calculate_amount("BYN", currency_buy, in_byn)
