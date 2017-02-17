#! /usr/bin/env python3
import json
import sys

import schemas
from concourse.common import Common
from serverless import Serverless


def execute(directory):
    common = Common()
    common.load_payload()
    common.directory = directory

    if not common.validate_payload(schemas.outSchema):
        return -1

    serverless = Serverless(common)
    serverless.set_credentials()

    payload = common.get_payload()

    result = 0

    if 'deploy' in payload['params'] and payload['params']['deploy']:
        result = serverless.deploy_service()

    if result != 0:
        return result

    if 'delete' in payload['params'] and payload['params']['delete']:
        serverless.delete_service()

    if result == 0:
        print(json.dumps({'version': {'ref': 'appName'}}))

    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        Common.log("Wrong number of arguments!")
        exit(-1)
    exit(execute(sys.argv[1]))
