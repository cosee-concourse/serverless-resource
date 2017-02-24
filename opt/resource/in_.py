#! /usr/bin/env python3
import json
import os
import sys

from concourse import common
from model import Model, Request
from serverless import Serverless


def execute(directory):
    try:
        model = Model(Request.IN)
    except TypeError:
        return -1

    serverless = Serverless(model, directory)
    serverless.set_credentials()

    with open(os.path.join(directory, "stage"), "w+") as file:
        file.write(model.get_stage_version())

    if model.get_stage_version() is None:
        print([{}])
    else:
        print(json.dumps({"version": {"stage": model.get_stage_version()}}))

    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        common.log_error("Wrong number of arguments!")
        exit(-1)
    exit(execute(sys.argv[1]))
