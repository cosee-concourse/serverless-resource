import unittest
from io import TextIOWrapper
from unittest.mock import MagicMock, patch

import in_
from concourse import test_common
from serverless import Serverless


class TestInput(unittest.TestCase):
    def setUp(self):
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

        self.assertEqual(in_.execute('/'), -1)

    def test_json(self):
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=TextIOWrapper)

            test_common.put_stdin(
                """
                {
                  "source": {
                    "access_key_id": "apiKey123",
                    "secret_access_key": "secretKey321"
                  },
                  "version": {
                    "stage": "1.0.0-rc.42"
                  }
                }
                """)

            self.assertEqual(in_.execute('/'), 0)
            file_handle = mock_open.return_value.__enter__.return_value
            file_handle.write.assert_called_with('1.0.0-rc.42')
