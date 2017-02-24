import unittest
from unittest.mock import MagicMock, patch

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
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
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
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              }
            }
            """)

        self.assertEqual(out.execute('/'), -1)

    @patch("out.shutil")
    def test_deploy(self, mock_shutil):
        Serverless.execute_command.return_value = 0

        test_common.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "stage": "version-v1-dev",
                "deploy": true,
                "artifact_folder": "artifact/lambda",
                "serverless_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        mock_shutil.copyfile.assert_called_with(r'/tmp/put/source/ci/serverless.yml', r'/tmp/put/artifact/lambda/serverless.yml')
        Serverless.execute_command.assert_called_with(['deploy', '--stage', 'version-v1-dev'], r'/tmp/put/artifact/lambda')

    def test_remove(self):
        Serverless.execute_command.return_value = 0

        test_common.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "stage": "version-v1-dev",
                "remove": true,
                "artifact_folder": "artifact/lambda",
                "serverless_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        Serverless.execute_command.assert_called_with(['remove', '--stage', 'version-v1-dev'], r'/tmp/put/source/ci')

    @patch("out.shutil")
    def test_json_deploy_region(self, mock_shutil):
        Serverless.execute_command.return_value = 0

        test_common.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321",
                "region_name": "eu-south-1"
              },
              "params": {
                "stage": "version-v1-dev",
                "deploy": true,
                "artifact_folder": "artifact/lambda",
                "serverless_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        mock_shutil.copyfile.assert_called_with("/tmp/put/source/ci/serverless.yml", "/tmp/put/artifact/lambda/serverless.yml")
        Serverless.execute_command.assert_called_with(
            ['deploy', '--stage', 'version-v1-dev', '--region', 'eu-south-1'], r'/tmp/put/artifact/lambda')


if __name__ == '__main__':
    unittest.main()
