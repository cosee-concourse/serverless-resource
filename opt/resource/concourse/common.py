import json
import os
import sys
import tempfile

from colorama import Back
from colorama import Fore
from jsonschema import Draft4Validator


def load_payload():
    payload = json.load(sys.stdin)
    _, file_name = tempfile.mkstemp()
    log_info("Logging payload to {}".format(file_name))
    with open(file_name, 'w') as fp:
        fp.write(json.dumps(payload))
    return payload


def validate_payload(payload,schema):
    return validate_json(payload, schema)


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def validate_json(input, schema):
    v = Draft4Validator(schema)

    valid = True

    for error in sorted(v.iter_errors(input), key=str):
        valid = False
        log_error("JSON Validation ERROR: " + error.message)

    if not valid:
        raise TypeError


def log_error(message):
    log(Fore.RED + str(message))


def log_warning(message):
    log(Fore.YELLOW + str(message))
    log(Fore.RED)


def log_info(message):
    log(Fore.BLUE + str(message))
    log(Fore.RED)