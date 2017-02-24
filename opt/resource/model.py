import os

from concourse import common
from enum import Enum
import schemas

VERSION_JSON_NAME = 'stage'


class Model:

    def __init__(self, request):
        self.payload = common.load_payload()
        self.directory = ''

        if request == Request.CHECK:
            schema = schemas.checkSchema
        elif request == Request.IN:
            schema = schemas.inSchema
        else:
            schema = schemas.outSchema

        common.validate_payload(self.payload, schema)

    def get_access_key(self):
        access_key = self.payload['source']['access_key_id']
        return access_key

    def get_secret(self):
        secret_key = self.payload['source']['secret_access_key']
        return secret_key

    def get_region_name(self):
        if 'region_name' in self.payload['source']:
            return self.payload['source']['region_name']
        return None

    def get_serverless_file(self):
        serverless_file = self.payload['params']['serverless_file']
        serverless_filepath = os.path.join(serverless_file, 'serverless.yml')
        return serverless_filepath

    def get_artifact_folder(self):
        artifact_folder = self.payload['params']['artifact_folder']
        return artifact_folder

    def get_stage_version(self):
        try:
            stage = self.payload['version'][VERSION_JSON_NAME]
        except KeyError:
            stage = None
        return stage


class Request(Enum):
    CHECK = 1
    IN = 2
    OUT = 3