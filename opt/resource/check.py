#! /usr/bin/env python3
from jsonschema import Draft4Validator

import schemas
from concourse.common import Common
from serverless import Serverless


def execute():
    common = Common()
    payload = common.get_payload()

    validation_result = validate(payload)
    if validation_result != 0:
        return validation_result

    serverless = Serverless(common)

    serverless.set_credentials()

    return 0


def validate(payload):
    v = Draft4Validator(schemas.checkSchema)
    valid = True

    for error in sorted(v.iter_errors(payload), key=str):
        Common.log(error.message)
        valid = False

    return 0 if valid else -1


if __name__ == '__main__':
    exit(execute())
