#! /usr/bin/env python3
import io
import json
from os import path
import shutil
import sys

from colorama import Fore
from colorama import init

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
        stage = io.open(path.join(directory, payload['params']['stageFile']), "r").read()
    elif 'stage' in payload['params']:
        stage = payload['params']['stage']
    else:
        Common.log("Requires stage or stageFile.")
        return -1

    serverless = Serverless(common, stage)
    serverless.set_credentials()

    result = 0

    serverless_filepath = path.join(directory, common.get_serverless_file())

    if 'deploy' in payload['params'] and payload['params']['deploy']:
        artifact_folder = path.join(directory,common.get_artifact_folder())
        shutil.copyfile(serverless_filepath, path.join(artifact_folder, path.basename(serverless_filepath)))
        common.directory = path.join(directory, artifact_folder)
        result = serverless.deploy_service()

    if result != 0:
        return result

    if 'remove' in payload['params'] and payload['params']['remove']:
        common.directory = path.dirname(serverless_filepath)
        serverless.remove_service()

    if result == 0:
        print(json.dumps({'version': {'stage': stage}}))

    return result


if __name__ == '__main__':
    init(autoreset=True)
    if len(sys.argv) < 2:
        Common.log(Fore.RED + "Wrong number of arguments!")
        exit(-1)
    exit(execute(sys.argv[1]))
