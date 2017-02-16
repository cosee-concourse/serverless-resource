from multiprocessing import Process
from subprocess import Popen, PIPE

from concourse.common import Common


class Serverless:
    def __init__(self, common):
        self.common = common

    def set_credentials(self):
        self.execute_command(['config', 'credentials',
                              '--provider', 'aws',
                              '--key', self.common.get_api_key(),
                              '--secret', self.common.get_secret()])

    @staticmethod
    def execute_command(command):
        commandToExecute = ['sls']
        commandToExecute.extend(command)

        def print_stderr(prog):
            for line in prog.stderr.readlines():
                Common.log(line.rstrip())

        def print_stdout(prog):
            """
            print stdout to stderr because only thing printed to stdout should be result json
            """
            for line in prog.stdout.readlines():
                Common.log(line.rstrip())

        p = Popen(commandToExecute, stdout=PIPE, stderr=PIPE)

        out_p = Process(target=print_stdout(p))
        out_e = Process(target=print_stderr(p))

        out_e.start()
        out_p.start()

        out_p.join()
        out_e.join()

        return p.returncode
