#! /usr/bin/env python3

import sys

import schemas
from concourse.common import Common
from serverless import Serverless


def execute(directory):
    common = Common()
    common.load_payload()

    if not common.validate_payload(schemas.inSchema):
        return -1

    serverless = Serverless(common, directory)
    serverless.set_credentials()

    print([{}])

    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        Common.log("Wrong number of arguments!")
        exit(-1)
    exit(execute(sys.argv[1]))
