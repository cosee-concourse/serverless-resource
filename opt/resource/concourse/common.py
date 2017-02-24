import json
import os
import sys
import tempfile

from colorama import Back
from colorama import Fore
from jsonschema import Draft4Validator


class Common:
    def __init__(self):
        self.payload = ''
        self.directory = ''

    def load_payload(self):
        payload = json.load(sys.stdin)
        _, file_name = tempfile.mkstemp()
        Common.log("Logging payload to {}".format(file_name))
        with open(file_name, 'w') as fp:
            fp.write(json.dumps(payload))
        self.payload = payload
        Common.log(Fore.YELLOW + str(payload))

    def get_payload(self):
        return self.payload

    def get_api_key(self):
        api_key = self.payload['source']['access_key_id']
        return api_key

    def get_secret(self):
        secret_key = self.payload['source']['secret_access_key']
        return secret_key

    def get_stage(self):
        try:
            stage = self.payload['version']['stage']
        except TypeError:
            stage = None
        return stage

    def get_region(self):
        if 'region_name' in self.payload['source']:
            return self.payload['source']['region_name']
        return None

    def get_serverless_file(self):
        serverless_file = self.payload['params']['serverless_file']
        serverless_filepath = os.path.join(serverless_file, 'serverless.yml')
        return serverless_filepath

    def get_artifact_folder(self):
        try:
            artifact_folder = self.payload['params']['artifact_folder']
        except KeyError:
            artifact_folder = None
        return artifact_folder

    def validate_payload(self, schema):
        return Common.validate_json(self.payload, schema)

    @staticmethod
    def log(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    @staticmethod
    def validate_json(payload, schema):
        v = Draft4Validator(schema)
        valid = True

        for error in sorted(v.iter_errors(payload), key=str):
            Common.log(Fore.WHITE + Back.RED + error.message)
            valid = False

        return valid
