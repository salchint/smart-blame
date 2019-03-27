#!python
# -*- coding: utf-8 -*-

import subprocess
import shlex


class BlameBlock:
    def __init__(self, blockIt):
        self._lines = [x for x in blockIt]
        self._lineCount = 0
        self._commitId = 0
        # print("Lines: ")
        # print(self._lines)

        # Decode the first line
        line = self._lines[0]
        fields = line.split()
        if 0 == len(fields):
            # print("No data in blame block")
            return
        elif 4 == len(fields):
            self._commitId, self._lineNoOrig, self._lineNoFinal, self._lineCount = fields
        else:
            self._commitId, self._lineNoOrig, self._lineNoFinal = fields

    def __repr__(self):
        return '\n'.join(self._lines)


    def commitId(self):
        return self._commitId

    def lineCount(self):
        return self._lineCount

    def sourceLine(self):
        # Take the last line and strip the leading tab
        return self._lines[-1][1:]


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
            if 0 == len(line):
                # Process a literally empty line
                yield line
                return
            if not line.startswith('\t'):
                # Process the header lines
                yield line
            else:
                # Process the single content line finally
                yield line
                return

    def getBlock(self):
        block = BlameBlock(self.iterPorcelain())
        return block

    def iterBlocks(self):
        while True:
            try:
                blockIt = self.iterPorcelain()
                block = BlameBlock(blockIt)
                if 0 == len(str(block)):
                    return
                yield block
            except:
                return

