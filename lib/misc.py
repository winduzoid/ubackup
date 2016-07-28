# coding: utf8

import re
import time

class Misc:

    def __init__(self, conf):
        self.md = time.strftime(conf.conf["date_format"] + ": ")

    def logDate(self, logfile):
        logfile.write(self.md)

# удаляем лишние слэши
def stsl(str):
    return re.sub('/+','/',str)

def myprint(str):
    sys.stdout.write(str)
    sys.stdout.flush()

