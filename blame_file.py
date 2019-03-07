import subprocess
import shlex

class Blame:
    def __init__(self, toBlame):
        self.gitArgs = "git blame --porcelain -- {}".format(toBlame)

    def run(self):
        try:
            return subprocess.check_output(
                shlex.split(self.gitArgs),
                stderr=subprocess.STDOUT,
                shell=True
            ).decode()
        except subprocess.CalledProcessError as e:
            #print "Failed to run '{}': ({}) {}".format(e.cmd, e.returncode, e.output.decode())
            print("Failed to run '{0}'".format(self.gitArgs))


