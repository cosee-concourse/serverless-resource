import unittest

import check
from concourse import test_common


class TestCheck(unittest.TestCase):
    def test_invalid_json(self):
        test_common.put_stdin(
            """
            {
               "sourcez":{
                  "apiKey": "apiKey123",
                  "secretKey": "secretKey321"
               },
               "version":{
                  "ref": "version-v1-dev"
               }
            }
            """)

        self.assertEqual(check.execute(), -1)

    def test_version_not_required_json(self):
        test_common.put_stdin(
            """
            {
               "source":{
                  "apiKey": "apiKey123",
                  "secretKey": "secretKey321"
               }
            }
            """)

        self.assertEqual(check.execute(), 0)

    def test_json(self):
        test_common.put_stdin(
            """
            {
               "source":{
                  "apiKey": "apiKey123",
                  "secretKey": "secretKey321"
               },
               "version":{
                  "ref": "version-v1-dev"
               }
            }
            """)

        self.assertEqual(check.execute(), 0)


if __name__ == '__main__':
    unittest.main()
