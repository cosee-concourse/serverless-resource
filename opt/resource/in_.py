#! /usr/bin/env python3

import os
import sys

from colorama import Fore
from colorama import init

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

    with open(os.path.join(directory, "stage"), "w+") as file:
        file.write(common.get_stage())

    print([{}])

    return 0


if __name__ == '__main__':
    init(autoreset=True)
    if len(sys.argv) < 2:
        Common.log(Fore.RED + "Wrong number of arguments!")
        exit(-1)
    exit(execute(sys.argv[1]))
