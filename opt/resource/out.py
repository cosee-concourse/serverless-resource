#! /usr/bin/env python3
import io
import json
import os
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

    payload = common.get_payload()

    if 'stageFile' in payload['params']:
        stage = io.open(os.path.join(directory, payload['params']['stageFile']), "r").read()
    elif 'stage' in payload['params']:
        stage = payload['params']['stage']
    else:
        Common.log("Requires stage or stageFile.")
        return -1

    serverless = Serverless(common, stage)
    serverless.set_credentials()

    result = 0

    if 'deploy' in payload['params'] and payload['params']['deploy']:
        result = serverless.deploy_service()

    if result != 0:
        return result

    if 'delete' in payload['params'] and payload['params']['delete']:
        serverless.delete_service()

    if result == 0:
        print(json.dumps({'version': {'stage': stage}}))

    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        Common.log("Wrong number of arguments!")
        exit(-1)
    exit(execute(sys.argv[1]))
