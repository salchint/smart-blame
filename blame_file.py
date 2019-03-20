#!python
# -*- coding: utf-8 -*-

import subprocess
import shlex


class BlameBlock:
    def __init__(self, block):
        _block = block


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
        pass


    # def getAnnotation(self):
        # return self.run().decode()

    # def getAnnotationBlock(self, beginning):
        # readChars = 0
        # annotation = self.getAnnotation()

        # # Annotation starts with a header of one or 12 lines
        # for line in annotation[beginning:].split('\n'):
            # readChars += len(line)
            # line = line.rstrip()

            # # Once we received the complete header, get the file content, which
            # # always starts with a TAB.
            # if line.startswith("\t"):
                # for contentLine in annotation[beginning+readChars:].split('\n'):
                    # readChars += len(contentLine)
                    # contentLine = contentLine.rstrip()
                    # if contentLine.startswith("\t"):
                        # yield contentLine

                # # The block is read
                # break
            # yield line

    # def getAnnotationBlocks(self):
        # beginning = 0
        # print("-" * 80)
        # for line in self.getAnnotationBlock(beginning):
            # print (line)

        # print("-" * 80)
