#! /usr/bin/env python3
import io
import json
import shutil
import sys
from os import path

from concourse import common
from model import Model, Request
from serverless import Serverless


def execute(directory):
    try:
        model = Model(Request.OUT)
    except TypeError:
        return -1

    if 'stageFile' in model.payload['params']:
        stage = io.open(path.join(directory, model.payload['params']['stageFile']), "r").read()
    elif 'stage' in model.payload['params']:
        stage = model.payload['params']['stage']
    else:
        common.log_error("Requires stage or stageFile.")
        return -1

    serverless = Serverless(model, stage)
    serverless.set_credentials()

    result = 0

    serverless_filepath = path.join(directory, model.get_serverless_file())

    if 'deploy' in model.payload['params'] and model.payload['params']['deploy']:
        artifact_folder = path.join(directory,model.get_artifact_folder())
        shutil.copyfile(serverless_filepath, path.join(artifact_folder, path.basename(serverless_filepath)))
        model.directory = path.join(directory, artifact_folder)
        result = serverless.deploy_service()

    if result != 0:
        return result

    if 'remove' in model.payload['params'] and model.payload['params']['remove']:
        model.directory = path.dirname(serverless_filepath)
        serverless.remove_service()

    if result == 0:
        print(json.dumps({'version': {'stage': stage}}))

    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        common.log_error("Wrong number of arguments!")
        exit(-1)
    exit(execute(sys.argv[1]))
