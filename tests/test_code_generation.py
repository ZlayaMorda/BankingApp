from django.test import TestCase
from django.core.cache import cache
from apps.authorization.services.code_generation import Code


class TestCode(TestCase):
    def test_generate_code_6(self):
        code = Code.generate_code_6()
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

    def test_store_load(self):
        jwt_token = 'some_jwt_token'

        # Test storing and loading a code
        code = Code.store(jwt_token)
        stored_jwt = Code.load(code)
        self.assertEqual(stored_jwt, jwt_token)

        # Test storing and loading multiple codes
        jwt_token_2 = 'another_jwt_token'
        code_2 = Code.store(jwt_token_2)
        stored_jwt_2 = Code.load(code_2)
        self.assertEqual(stored_jwt_2, jwt_token_2)

        # Test loading non-existent code
        non_existent_code = '000000'
        non_existent_jwt = Code.load(non_existent_code)
        self.assertIsNone(non_existent_jwt)

        # Test loading code after clearing cache
        cache.clear()
        cleared_jwt = Code.load(code)
        self.assertIsNone(cleared_jwt)
