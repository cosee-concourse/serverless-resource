import sys
import unittest
from io import StringIO

from concourse import common


class TestCommon(unittest.TestCase):
    standard_payload = (
        """
        {
        "source": {
            "apiKey": "apiKey123",
            "secretKey": "secretKey321"
            },
            "version": {
                "ref": "version-v1-dev"
            }
        }
        """)

    def setUp(self):
        self.common_instance = common.Common()

    def test_getPayload(self):
        put_stdin(self.standard_payload)
        result = self.common_instance.get_payload()
        self.assertEqual(result['source']['apiKey'], "apiKey123")
        self.assertEqual(result['source']['secretKey'], "secretKey321")
        self.assertEqual(result['version']['ref'], "version-v1-dev")

    def test_getApiKey(self):
        put_stdin(self.standard_payload)
        self.common_instance.get_payload()
        api_key = self.common_instance.get_api_key()
        self.assertEqual(api_key, "apiKey123")

    def test_getSecretKey(self):
        put_stdin(self.standard_payload)
        self.common_instance.get_payload()
        secret_key = self.common_instance.get_secret()
        self.assertEqual(secret_key, "secretKey321")


def put_stdin(content):
    sys.stdin = StringIO(content)


if __name__ == '__main__':
    unittest.main()
