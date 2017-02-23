import os
from multiprocessing import Process
from subprocess import Popen, PIPE

from concourse.common import Common


class Serverless:
    def __init__(self, common, stage=None):
        self.common = common
        self.stage = stage

    def set_credentials(self):
        return self.execute_command(['config', 'credentials',
                                     '--provider', 'aws',
                                     '--key', self.common.get_api_key(),
                                     '--secret', self.common.get_secret()])

    def deploy_service(self):
        if self.common.directory is '':
            Common.log("Directory is not set.")
            return -1

        deploy_command = ['deploy']
        if self.stage is not None:
            deploy_command.extend(['--stage', self.stage])

        region = self.common.get_region()
        if region is not None:
            deploy_command.extend(['--region', region])

        return self.execute_command(deploy_command, self.common.directory)

    def remove_service(self):
        if self.common.directory is '':
            Common.log("Directory is not set.")
            return -1

        remove_command = ['remove']
        if self.stage is not None:
            remove_command.extend(['--stage', self.stage])

        region = self.common.get_region()
        if region is not None:
            remove_command.extend(['--region', region])

        return self.execute_command(remove_command, self.common.directory)

    def execute_command(self, command, directory=None):
        exec_command = ['sls']
        exec_command.extend(command)

        slsEnv = os.environ.copy()
        if self.stage is not None:
            slsEnv['STAGE'] = self.stage

        def print_stderr(prog):
            for line in prog.stderr.readlines():
                Common.log(line.rstrip().decode('ascii'))

        def print_stdout(prog):
            """
            print stdout to stderr because only thing printed to stdout should be result json
            """
            for line in prog.stdout.readlines():
                Common.log(line.rstrip().decode('ascii'))

        p = Popen(exec_command, stdout=PIPE, stderr=PIPE, env=slsEnv, cwd=directory or '/')

        out_p = Process(target=print_stdout(p))
        out_e = Process(target=print_stderr(p))

        out_e.start()
        out_p.start()

        out_p.join()
        out_e.join()

        p.communicate()
        Common.log("{} exited with {}".format(exec_command, p.returncode))

        return p.returncode
