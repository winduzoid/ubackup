# coding: utf8

import re
import time
import os

class Misc:
    def __init__(self, conf):
        self.conf = conf

    def md(self):
        return time.strftime(self.conf.conf["date_format"] + ": ")

    def logDate(self, logfile):
        logfile.write(self.md())

# removing redundant slashes
def stsl(str):
    return re.sub('/+','/',str)

def myprint(str):
    sys.stdout.write(str)
    sys.stdout.flush()

def showVersion():
    versionFile = os.path.dirname(os.path.realpath(__file__)) + "/assets/VERSION"
    fd = open(versionFile, "r")
    print "Ubackup version %s" % fd.readline().strip("\n")
    fd.close()
