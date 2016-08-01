# coding: utf8

import re
import time

class Misc:

    def __init__(self, conf):
        self.md = time.strftime(conf.conf["date_format"] + ": ")

    def logDate(self, logfile):
        logfile.write(self.md)

# removing redundant slashes
def stsl(str):
    return re.sub('/+','/',str)

def myprint(str):
    sys.stdout.write(str)
    sys.stdout.flush()

