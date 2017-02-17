from multiprocessing import Process
from subprocess import Popen, PIPE

from concourse.common import Common


class Serverless:
    def __init__(self, common):
        self.common = common

    def set_credentials(self):
        return self.execute_command(['config', 'credentials',
                                     '--provider', 'aws',
                                     '--key', self.common.get_api_key(),
                                     '--secret', self.common.get_secret()])

    def deploy_service(self):
        if self.common.directory is '':
            Common.log("Directory is not set.")
            return -1

        return self.execute_command(['deploy'], self.common.directory)

    def delete_service(self):
        if self.common.directory is '':
            Common.log("Directory is not set.")
            return -1

        return self.execute_command(['delete'], self.common.directory)

    @staticmethod
    def execute_command(command, directory=None):
        commandToExecute = ['sls']
        commandToExecute.extend(command)

        def print_stderr(prog):
            for line in prog.stderr.readlines():
                Common.log(line.rstrip().decode('ascii'))

        def print_stdout(prog):
            """
            print stdout to stderr because only thing printed to stdout should be result json
            """
            for line in prog.stdout.readlines():
                Common.log(line.rstrip().decode('ascii'))

        p = Popen(commandToExecute, stdout=PIPE, stderr=PIPE, shell=True, cwd=directory or '/')

        out_p = Process(target=print_stdout(p))
        out_e = Process(target=print_stderr(p))

        out_e.start()
        out_p.start()

        out_p.join()
        out_e.join()

        p.communicate()
        Common.log("{} exited with {}".format(command, p.returncode))

        return p.returncode
