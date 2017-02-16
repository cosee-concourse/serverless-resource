#! /usr/bin/env python3

import schemas
from concourse.common import Common
from serverless import Serverless


def execute():
    common = Common()
    common.load_payload()

    if not common.validate_payload(schemas.checkSchema):
        return -1

    serverless = Serverless(common)
    serverless.set_credentials()

    return 0


if __name__ == '__main__':
    exit(execute())
