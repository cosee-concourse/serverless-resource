import unittest

import out
from concourse import test_common


class TestOut(unittest.TestCase):
    def test_invalid_json(self):
        test_common.put_stdin(
            """
            {
              "source": {
                "apiKey": "apiKey123",
                "secretKey": "secretKey321"
              }
            }
            """)

        self.assertEqual(out.execute(), -1)

    def test_params_required_json(self):
        test_common.put_stdin(
            """
            {
              "source": {
                "apiKey": "apiKey123",
                "secretKey": "secretKey321"
              }
            }
            """)

        self.assertEqual(out.execute(), -1)

    def test_json(self):
        test_common.put_stdin(
            """
            {
              "source": {
                "apiKey": "apiKey123",
                "secretKey": "secretKey321"
              },
              "params": {
                "appFile": "version-v1-dev",
                "deploy": true
              }
            }
            """)

        self.assertEqual(out.execute(), 0)


if __name__ == '__main__':
    unittest.main()
