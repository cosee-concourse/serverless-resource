import unittest
from unittest.mock import MagicMock

from colorama import init

import out
from concourse import test_common
from serverless import Serverless


class TestOut(unittest.TestCase):
    def setUp(self):
        init(autoreset=True)
        Serverless.execute_command = MagicMock(name='execute_command')

    def test_invalid_json(self):
        test_common.put_stdin(
            """
            {
              "source": {
                "apiKey": "apiKey123",
                "secretKey": "secretKey321"
              },
              "params": {
              }
            }
            """)

        self.assertEqual(out.execute('/'), -1)

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

        self.assertEqual(out.execute('/'), -1)

    def test_json(self):
        Serverless.execute_command.return_value = 0

        test_common.put_stdin(
            """
            {
              "source": {
                "apiKey": "apiKey123",
                "secretKey": "secretKey321"
              },
              "params": {
                "stage": "version-v1-dev",
                "deploy": true,
                "directory": "artifact/lambda"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        Serverless.execute_command.assert_called_with(['deploy', '--stage', 'version-v1-dev'], r'/tmp/put/')

    def test_json_region(self):
        Serverless.execute_command.return_value = 0

        test_common.put_stdin(
            """
            {
              "source": {
                "apiKey": "apiKey123",
                "secretKey": "secretKey321",
                "region": "eu-south-1"
              },
              "params": {
                "stage": "version-v1-dev",
                "deploy": true,
                "directory": "artifact/lambda"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        Serverless.execute_command.assert_called_with(
            ['deploy', '--stage', 'version-v1-dev', '--region', 'eu-south-1'], r'/tmp/put/')


if __name__ == '__main__':
    unittest.main()
