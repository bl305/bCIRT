# https://www.daniweb.com/programming/software-development/code/257449/a-command-class-to-run-shell-commands
# https://pymotw.com/2/argparse/
from subprocess import Popen, PIPE, STDOUT


class run_script_class(object):
    """
    Run a python script and capture its output string, error string and exit status
    input: interpreter, command, argument="", timeout=300
    output:

    """
    def __init__(self, interpreter, command, argument=None, timeout=300):
        self.commandline = str(interpreter)
        if command != "None":
            self.commandline = self.commandline + " " + str(command)
            print(self.commandline)
        if argument != "None" and argument != "":
            self.commandline = self.commandline + " " + str(argument)
            print(self.commandline)
        self.command = self.commandline.split()
        self.timeout = timeout

    def runscript(self):
        """
        runs a script using the given parameters
        :input: command, timeout
        :return: {{"command:": X, "status": S, "error": E, "output": O, "PID": P}}
        """
        try:
            process = Popen(self.command, universal_newlines=True, stdout=PIPE, stderr=STDOUT)
            pid = process.pid
            process.wait(self.timeout)
            self.output, self.error = process.communicate()
            self.status = process.returncode
            # self.exitstatus = process.poll()
        except Exception as e:
            return {"command": self.command, "status": "1", "error": "1", "output": str(e)}
        if self.error == None:
            return {"command": self.command, "status": self.status, "error": "0", "output": self.output, "pid": pid}
        else:
            return {"command": self.command, "status": self.status, "error": self.error, "output": self.output, "pid": pid}

    def runcmd(self):
        """
        runs a script using the given parameters
        :input: command, timeout
        :return: {{"command:": X, "status": S, "error": E, "output": O, "PID": P}}
        """
        try:
            process = Popen(self.commandline, shell=True, universal_newlines=True, stdout=PIPE, stderr=STDOUT)
            pid = process.pid
            process.wait(self.timeout)
            self.output, self.error = process.communicate()
            self.status = process.returncode
            # self.exitstatus = process.poll()
        except Exception as e:
            return {"command": self.command, "status": "1", "error": "1", "output": str(e)}
        if self.error == None:
            return {"command": self.command, "status": self.status, "error": "0", "output": self.output, "pid": pid}
        else:
            return {"command": self.command, "status": self.status, "error": self.error, "output": self.output, "pid": pid}
