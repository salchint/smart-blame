import subprocess
import shlex

class Blame:
    def __init__(self):
        self.gitArgs = "git annotate --porcelain -- {}"

    def run(self):
        try:
            return subprocess.check_output(shlex.split(self.gitArgs.format("smart-blame.py")), stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as e:
            #print "Failed to run '{}': ({}) {}".format(e.cmd, e.returncode, e.output.decode())
            print("Failed to run '{0}'".format(self.gitArgs))


