import json
import unittest
from unittest.mock import patch, Mock
from apps.credit.services.third_party_api import CreditAPI, NotFound


class TestCreditAPI(unittest.TestCase):
    @patch('requests.get')
    def test_get_last_refinancing_rate_success(self, mock_get):
        # Mocking a successful API response
        mock_response = Mock()
        mock_response.content = json.dumps([{"Value": "5.25"}]).encode('utf-8')
        mock_get.return_value = mock_response

        credit_api = CreditAPI()
        rate = credit_api.get_last_refinancing_rate()
        self.assertEqual(rate, 5.25)

        # Ensure requests.get was called with the correct URL
        mock_get.assert_called_once_with("https://api.nbrb.by/refinancingrate")

    @patch('requests.get')
    def test_get_last_refinancing_rate_empty_response(self, mock_get):
        # Mocking an empty API response
        mock_response = Mock()
        mock_response.content = json.dumps([]).encode('utf-8')
        mock_get.return_value = mock_response

        credit_api = CreditAPI()
        with self.assertRaises(NotFound):
            credit_api.get_last_refinancing_rate()

    @patch('requests.get')
    def test_get_last_refinancing_rate_invalid_response(self, mock_get):
        # Mocking an invalid API response (not JSON)
        mock_response = Mock()
        mock_response.content = "Invalid content"
        mock_get.return_value = mock_response

        credit_api = CreditAPI()
        with self.assertRaises(NotFound):
            credit_api.get_last_refinancing_rate()

    @patch('requests.get')
    def test_get_last_refinancing_rate_request_failure(self, mock_get):
        # Mocking a failed request
        mock_get.side_effect = Exception("Failed to connect")

        credit_api = CreditAPI()
        with self.assertRaises(NotFound):
            credit_api.get_last_refinancing_rate()

