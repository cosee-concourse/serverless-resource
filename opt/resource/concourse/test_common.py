import unittest

from concourse import common, testutil


class TestCommon(unittest.TestCase):
    standard_payload = (
        """
        {
        "source": {
            "access_key_id": "apiKey123",
            "secret_access_key": "secretKey321"
            },
            "version": {
                "ref": "version-v1-dev"
            }
        }
        """)

    def test_getPayload(self):
        testutil.put_stdin(self.standard_payload)
        result = common.load_payload()
        self.assertEqual(result['source']['access_key_id'], "apiKey123")
        self.assertEqual(result['source']['secret_access_key'], "secretKey321")
        self.assertEqual(result['version']['ref'], "version-v1-dev")


if __name__ == '__main__':
    unittest.main()
