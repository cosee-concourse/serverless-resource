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

    if model.stage_file_exists():
        stage = io.open(path.join(directory, model.get_stage_file()), "r").read()
    elif model.stage_name_exists():
        stage = model.get_stage_name()
    else:
        common.log_error("Requires stage or stage_file.")
        return -1

    serverless = Serverless(model, stage)
    serverless.set_credentials()

    result = 0

    serverless_filepath = path.join(directory, model.get_serverless_file())

    if model.is_deploy_command():
        artifact_folder = path.join(directory,model.get_artifact_folder())

        # copies serverless file to artifact folder
        shutil.copyfile(serverless_filepath, path.join(artifact_folder, path.basename(serverless_filepath)))

        model.directory = path.join(directory, artifact_folder)
        result = serverless.deploy_service()

    if result != 0:
        return result

    if model.is_remove_command():
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
