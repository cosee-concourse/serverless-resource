import unittest
from unittest.mock import MagicMock

import check
from concourse import test_common
from serverless import Serverless


class TestCheck(unittest.TestCase):
    def setUp(self):
        Serverless.execute_command = MagicMock(name='execute_command')

    def test_invalid_json(self):
        test_common.put_stdin(
            """
            {
               "sourcez":{
                  "apiKey": "apiKey123",
                  "secretKey": "secretKey321"
               },
               "version":{
                  "schema": "version-v1-dev"
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

    def test_version_is_null(self):
        test_common.put_stdin(
            """
            {
               "source":{
                  "apiKey": "apiKey123",
                  "secretKey": "secretKey321"
               },
               "version": null
            }
            """)

        self.assertEqual(check.execute(), 0)

    def test_version_is_empty(self):
        test_common.put_stdin(
            """
            {
               "source":{
                  "apiKey": "apiKey123",
                  "secretKey": "secretKey321"
               },
               "version": {}
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
                  "schema": "version-v1-dev"
               }
            }
            """)

        self.assertEqual(check.execute(), 0)
        Serverless.execute_command.assert_called_once_with(['config', 'credentials',
                                                            '--provider', 'aws',
                                                            '--key', 'apiKey123',
                                                            '--secret', 'secretKey321'])


if __name__ == '__main__':
    unittest.main()
