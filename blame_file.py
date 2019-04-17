#!python
# -*- coding: utf-8 -*-

import subprocess
import shlex


class PorcelainBlock:
    """A PorcelainBlock encapsulates the deserialized fields of a block of
    annotation information attached to a line of code."""

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

    def lineNumber(self):
        return self._lineNoFinal


class Blame:
    """This class issues the blame command and collects the result textual
    result.

    It can be used to iterate through git's output line by line. But it
    includes some logic on its own to interpret the git-blame's porcelain
    output. So the alternative is to iterate through the porcelain 'blocks'
    """

    def __init__(self, toBlame, commit=""):
        if 0 < len(commit):
            self.gitArgs = "git blame --porcelain {} -- {}".format(commit, toBlame)
        else:
            self.gitArgs = "git blame --porcelain -- {}".format(toBlame)
        self._readOffset = 0
        self._annotated = self.run().decode()

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
        for line in self._annotated[offset:].split('\n'):
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
        block = PorcelainBlock(self.iterPorcelain())
        return block

    def iterBlocks(self):
        while True:
            try:
                blockIt = self.iterPorcelain()
                block = PorcelainBlock(blockIt)
                if 0 == len(str(block)):
                    return
                yield block
            except:
                return

