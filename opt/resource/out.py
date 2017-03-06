#! /usr/bin/env python3
import shutil
from os import path

from concourse_common import ioutil
from concourse_common.common import *
from concourse_common.jsonutil import *

import schemas
from model import *
from serverless import Serverless
from s3blanker import S3Blanker


SERVERLESS_CONFIG_FILENAME = 'serverless.yml'


def is_deploy_command(payload):
    if contains_params_key(payload, DEPLOY_KEY):
        return get_params_value(payload, DEPLOY_KEY)
    return False


def is_remove_command(payload):
    if contains_params_key(payload, REMOVE_KEY):
        return get_params_value(payload, REMOVE_KEY)
    return False


def execute(directory):
    valid, payload = load_and_validate_payload(schemas, Request.OUT)
    if not valid:
        return -1

    if contains_params_key(payload, STAGE_FILE_KEY):
        stage = ioutil.read_file(path.join(directory, get_params_value(payload, STAGE_FILE_KEY)))
    elif contains_params_key(payload, STAGE_KEY):
        stage = get_params_value(payload, STAGE_KEY)
    else:
        log_error("Requires stage or stage_file.")
        return -1

    serverless = Serverless(payload, directory, stage)
    serverless.set_credentials()

    result = 0

    serverless_filepath = path.join(directory, get_params_value(payload, SERVERLESS_FILE_KEY),
                                    SERVERLESS_CONFIG_FILENAME)

    if not validate_path(serverless_filepath):
        log_error("Serverless config does not exist")
        return -1

    if is_deploy_command(payload):
        artifact_folder = path.join(directory, get_params_value(payload, ARTIFACT_FOLDER_KEY))

        # copies serverless file to artifact folder
        shutil.copyfile(serverless_filepath, path.join(artifact_folder, path.basename(serverless_filepath)))

        serverless.directory = path.join(directory, artifact_folder)
        result = serverless.deploy_service()

    if result != 0:
        return result

    if is_remove_command(payload):
        blanker = S3Blanker(get_source_value(payload, ACCESS_KEY), get_source_value(payload, SECRET_KEY))
        blanker.empty_buckets_for_serverless_config(serverless_filepath, stage)
        serverless.directory = path.dirname(serverless_filepath)
        serverless.remove_service()

    if result == 0:
        print(get_version_output('stage', VERSION_KEY_NAME))

    return result


if __name__ == '__main__':
    if not check_system_argument_number():
        exit(-1)
    exit(execute(sys.argv[1]))
