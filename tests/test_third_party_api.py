import json
import unittest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from requests.exceptions import RequestException
from apps.account.services.third_party_api import ExchangeRateAPI
from utils.exceptions import NotFound

class TestExchangeRateAPI(unittest.TestCase):
    @patch('requests.get')
    def test_get_today_rates(self, mock_requests_get):
        # Mock successful API response
        mock_content = [
            {"Cur_Abbreviation": "USD", "Cur_OfficialRate": 2.0},
            {"Cur_Abbreviation": "EUR", "Cur_OfficialRate": 3.0}
        ]
        mock_requests_get.return_value.content = bytes(json.dumps(mock_content), 'utf-8')

        exchange_rate_api = ExchangeRateAPI()
        rates = exchange_rate_api.get_today_rates()

        self.assertEqual(rates['USD'], Decimal('2.0'))
        self.assertEqual(rates['EUR'], Decimal('3.0'))

        # Mock scenario where rate fetching fails
        mock_requests_get.side_effect = RequestException()

        with self.assertRaises(NotFound):
            exchange_rate_api.get_today_rates()

    def test_calculate_amount(self):
        exchange_rate_api = ExchangeRateAPI()
        exchange_rate_api.get_today_rates = MagicMock(return_value={'USD': Decimal('2.0'), 'EUR': Decimal('3.0')})

        # Test currency_sell equals currency_buy
        result = exchange_rate_api.calculate_amount('USD', 'USD', 50)
        self.assertEqual(result, 50)

        # Test currency_sell is BYN
        result = exchange_rate_api.calculate_amount('BYN', 'USD', 100)
        self.assertEqual(result, round(100 / (Decimal('2.0') * exchange_rate_api.coef), 2))

        # Test currency_buy is BYN
        result = exchange_rate_api.calculate_amount('USD', 'BYN', 100)
        self.assertEqual(result, round(100 * Decimal('2.0'), 2))

        # Test other scenarios
        exchange_rate_api.calculate_amount = MagicMock(side_effect=exchange_rate_api.calculate_amount)
        result = exchange_rate_api.calculate_amount('EUR', 'USD', 100)
        self.assertEqual(result, round(100 * Decimal('3.0') / (Decimal('2.0') * exchange_rate_api.coef), 2))
