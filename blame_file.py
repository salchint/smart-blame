#!python
# -*- coding: utf-8 -*-

import subprocess
import shlex


class BlameBlock:
    def __init__(self, block, lineCnt=0):
        self._blockIt = block
        self._lineCount = lineCnt

        # Decode the first line
        line = self._blockIt.__next__()
        fields = line.split()
        if 4 == len(fields):
            self._commitId, self._lineNoOrig, self._lineNoFinal, self._lineCount = fields
        else:
            self._commitId, self._lineNoOrig, self._lineNoFinal = fields

        # print ("Commit: {}".format(self._commitId))
        # print ("Line  : {}".format(self._lineNoOrig))
        # print ("Line  : {}".format(self._lineNoFinal))
        # print ("Lines : {}".format(self._lineCount))

    def __repr__(self):
        s = "\n".join(self._blockIt)
        return s


class Blame:
    def __init__(self, toBlame):
        self.gitArgs = "git blame --porcelain -- {}".format(toBlame)
        self._readOffset = 0

    def run(self):
        try:
            output = subprocess.check_output(
                shlex.split(self.gitArgs),
                stderr=subprocess.STDOUT,
                shell=False
            )
            #print(output)
            return output
        except subprocess.CalledProcessError as e:
            #print("Failed to run '{0}'".format(self.gitArgs))
            print("Failed to run '{0}': ({1}) {2}".format(e.cmd, e.returncode, e.output.decode()))

    def iterLine(self, offset):
        annotated = self.run().decode()
        for line in annotated[offset:].split('\n'):
            self._readOffset += len(line) + 1
            line = line.rstrip()
            yield line

    def iterPorcelain(self):
        for line in self.iterLine(self._readOffset):
            if not line.startswith('\t'):
                # Process the header lines
                yield line
            else:
                # Process the single content line finally
                yield line
                return

    def getBlock(self):
        block = BlameBlock(self.iterPorcelain())
        # print (block)
        return block


