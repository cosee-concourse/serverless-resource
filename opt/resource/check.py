#! /usr/bin/env python3
from model import Model, Request
from serverless import Serverless


def execute():
    try:
        model = Model(Request.CHECK)
    except TypeError:
        return -1

    serverless = Serverless(model)
    serverless.set_credentials()

    print([{}])

    return 0


if __name__ == '__main__':
    exit(execute())
