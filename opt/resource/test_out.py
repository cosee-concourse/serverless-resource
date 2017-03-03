import unittest
from unittest.mock import MagicMock, patch

import out
from concourse_common import testutil
from serverless import Serverless


class TestOut(unittest.TestCase):
    def setUp(self):
        Serverless.execute_command = MagicMock(name='execute_command')

    def test_invalid_json(self):
        testutil.put_stdin(
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
        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              }
            }
            """)

        self.assertEqual(out.execute('/'), -1)

    def test_deploy_artifact_folder_needed(self):
        Serverless.execute_command.return_value = 0

        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "stage": "version-v1-dev",
                "deploy": true,
                "serverless_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute('/'), -1)

    def test_deploy_stage_needed(self):
        Serverless.execute_command.return_value = 0

        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "deploy": true,
                "serverless_file": "source/ci/",
                "artifact_folder": "artifacts/"

              }
            }
            """)

        self.assertEqual(out.execute('/'), -1)

    def test_deploy_operation_needed(self):
        Serverless.execute_command.return_value = 0

        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "stage": "release",
                "serverless_file": "source/ci/",
                "artifact_folder": "artifacts/"

              }
            }
            """)

        self.assertEqual(out.execute('/'), -1)

    @patch("out.validate_path")
    @patch("out.shutil")
    def test_deploy(self, mock_shutil, mock_validate_filepath):
        Serverless.execute_command.return_value = 0
        mock_validate_filepath.return_value = True
        testutil.put_stdin(
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
        mock_shutil.copyfile.assert_called_with(r'/tmp/put/source/ci/serverless.yml',
                                                r'/tmp/put/artifact/lambda/serverless.yml')
        Serverless.execute_command.assert_called_with(['deploy', '--stage', 'version-v1-dev'],
                                                      r'/tmp/put/artifact/lambda')

    @patch("out.validate_path")
    @patch("io.open")
    @patch("out.shutil")
    def test_deploy_with_stage_file(self, mock_shutil, mock_io_open, mock_validate_path):
        Serverless.execute_command.return_value = 0
        mock_file = MagicMock()
        mock_io_open.return_value = mock_file
        mock_file.read.return_value = "release"
        mock_validate_path.return_value = True

        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "stage_file": "naming/stage",
                "deploy": true,
                "artifact_folder": "artifact/lambda",
                "serverless_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        mock_shutil.copyfile.assert_called_with(r'/tmp/put/source/ci/serverless.yml',
                                                r'/tmp/put/artifact/lambda/serverless.yml')
        Serverless.execute_command.assert_called_with(['deploy', '--stage', 'release'], r'/tmp/put/artifact/lambda')

    @patch("out.validate_path")
    def test_remove(self, mock_validate_path):
        Serverless.execute_command.return_value = 0
        mock_validate_path.return_value = True

        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "stage": "version-v1-dev",
                "remove": true,
                "serverless_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        Serverless.execute_command.assert_called_with(['remove', '--stage', 'version-v1-dev'], r'/tmp/put/source/ci')


    @patch("out.validate_path")
    @patch("io.open")
    def test_remove_with_stage_file(self, mock_io_open, mock_validate_path):
        Serverless.execute_command.return_value = 0
        mock_file = MagicMock()
        mock_io_open.return_value = mock_file
        mock_file.read.return_value = "release"
        mock_validate_path.return_value = True

        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "stage_file": "release",
                "remove": true,
                "serverless_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        Serverless.execute_command.assert_called_with(['remove', '--stage', 'release'], r'/tmp/put/source/ci')

    @patch("out.validate_path")
    @patch("out.shutil")
    def test_deploy_with_region(self, mock_shutil, mock_validate_filepath):
        Serverless.execute_command.return_value = 0
        mock_validate_filepath.return_value = True

        testutil.put_stdin(
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
        mock_shutil.copyfile.assert_called_with("/tmp/put/source/ci/serverless.yml",
                                                "/tmp/put/artifact/lambda/serverless.yml")
        Serverless.execute_command.assert_called_with(
            ['deploy', '--stage', 'version-v1-dev', '--region', 'eu-south-1'], r'/tmp/put/artifact/lambda')


if __name__ == '__main__':
    unittest.main()
