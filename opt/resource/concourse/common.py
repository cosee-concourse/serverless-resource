import json
import sys
import tempfile

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
        Common.log(payload)

    def get_payload(self):
        return self.payload

    def get_api_key(self):
        api_key = self.payload['source']['apiKey']
        return api_key

    def get_secret(self):
        secret_key = self.payload['source']['secretKey']
        return secret_key

    def get_version(self):
        try:
            version = self.payload['version']['version']
        except TypeError:
            version = None
        return version

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
            Common.log(error.message)
            valid = False

        return valid
