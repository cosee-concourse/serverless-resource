#! /usr/bin/env python3
from model import *
from concourse_common.jsonutil import *
from serverless import Serverless
import schemas

def execute():
    valid, payload = load_and_validate_payload(schemas, Request.CHECK)
    if not valid:
        return -1

    serverless = Serverless(payload, None)
    serverless.set_credentials()

    print([{}])

    return 0


if __name__ == '__main__':
    exit(execute())
