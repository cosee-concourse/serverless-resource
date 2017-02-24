import unittest

from concourse import testutil

from model import Model, Request
import payloads


class TestModel(unittest.TestCase):
    def setUpGetterTest(self, payload, request):
        testutil.put_stdin(payload)
        self.model = Model(request)

    def test_get_access_key(self):
        self.setUpGetterTest(payloads.check_payload, Request.CHECK)
        api_key = self.model.get_access_key()
        self.assertEqual(api_key, "apiKey123")

    def test_get_secret_key(self):
        self.setUpGetterTest(payloads.check_payload, Request.CHECK)
        secret_key = self.model.get_secret()
        self.assertEqual(secret_key, "secretKey321")

    def test_get_region_name(self):
        self.setUpGetterTest(payloads.check_payload, Request.CHECK)
        region_name = self.model.get_region_name()
        self.assertEqual(region_name, "eu-west-1")

    def test_get_stage_version(self):
        self.setUpGetterTest(payloads.check_payload, Request.CHECK)
        version = self.model.get_stage_version()
        self.assertEqual(version, "release")

    def test_get_serverlessfile(self):
        self.setUpGetterTest(payloads.out_deploy_payload, Request.OUT)
        version = self.model.get_serverless_file()
        self.assertEqual(version, "source/ci/serverless.yml")

    def test_get_artifact_folder(self):
        self.setUpGetterTest(payloads.out_deploy_payload, Request.OUT)
        version = self.model.get_artifact_folder()
        self.assertEqual(version, "artifact/lambda")


if __name__ == '__main__':
    unittest.main()
