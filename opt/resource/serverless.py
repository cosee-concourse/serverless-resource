from subprocess import Popen, PIPE

from concourse_common.common import *
from concourse_common.jsonutil import *

from model import *


class Serverless:
    def __init__(self, payload, directory, stage=None):
        self.payload = payload
        self.directory = directory
        self.stage = stage

    def set_credentials(self):
        return self.execute_command(['config', 'credentials',
                                     '--provider', 'aws',
                                     '--key', get_source_value(self.payload, ACCESS_KEY),
                                     '--secret', get_source_value(self.payload, SECRET_KEY)])

    def deploy_service(self):
        if self.directory is '':
            log_error("Directory is not set.")
            return -1

        deploy_command = ['deploy']
        if self.stage is not None:
            deploy_command.extend(['--stage', self.stage])

        region = get_source_value(self.payload, REGION_NAME_KEY)
        if region is not None:
            deploy_command.extend(['--region', region])

        return self.execute_command(deploy_command, self.directory)

    def remove_service(self):
        if self.directory is '':
            log_error("Directory is not set.")
            return -1

        remove_command = ['remove']
        if self.stage is not None:
            remove_command.extend(['--stage', self.stage])

        region = get_source_value(self.payload, REGION_NAME_KEY)
        if region is not None:
            remove_command.extend(['--region', region])

        return self.execute_command(remove_command, self.directory)

    def execute_command(self, command, directory=None):
        exec_command = ['sls']
        exec_command.extend(command)

        slsEnv = os.environ.copy()
        if self.stage is not None:
            slsEnv['STAGE'] = self.stage
            slsEnv['BUCKET_NAME'] = self.stage

        p = Popen(exec_command, stdout=PIPE, stderr=PIPE, env=slsEnv, cwd=directory or '/', universal_newlines=True)

        out, err = p.communicate()
        log_info(out)
        log_error(err)

        log_info("{} exited with {}".format(exec_command[0:2], p.returncode))

        return p.returncode
