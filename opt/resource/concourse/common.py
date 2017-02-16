import json
import sys
import tempfile


class Common:
    def __init__(self):
        self.payload = ""

    def get_payload(self):
        payload = json.load(sys.stdin)
        _, file_name = tempfile.mkstemp()
        Common.log("Logging payload to {}".format(file_name))
        with open(file_name, 'w') as fp:
            fp.write(json.dumps(payload))
        self.payload = payload
        Common.log(payload)

        return payload

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

    @staticmethod
    def log(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
