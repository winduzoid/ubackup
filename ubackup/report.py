# coding: utf8

import sys

from ubackup.misc import *

class ReportItem:
    
    def __init__(self, name = None, debug = None):
        self.debug = debug
        self.data = {}
        self.data["name"] = name

    def set(self, name, uvalue):
        self.data[name] = uvalue

    def show(self):
        print self.data


class Report:
    def __init__(self, conf, debug = None):
        self.conf = conf
        self.debug = debug
        self.reportItem = []
        self.data = {}
    
    def add(self, reportItem):
        self.reportItem.append(reportItem)

    def set(self, name, uvalue):
        self.data[name] = uvalue

    def generate(self):
        misc = Misc(self.conf)
        print "Report\n"
        duration = self.data["TimeFinish"] - self.data["TimeStart"]
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        print("Duration: %02d:%02d:%02d (%s - %s)" % (hours, minutes, seconds, misc.md(self.data["TimeStart"], delim=''), misc.md(self.data["TimeFinish"], delim='')))
        if self.debug:
            for i in sorted(self.data):
                print "%s: %s" % (i, self.data[i])
        else:
            print "DryRun: %s" % self.data["DryRun"]
        print "\nHosts:"
        for i in self.reportItem:
            sys.stdout.write("Host name = %s" % i.data["name"])
            try:
                sys.stdout.write(", Return code: %d" % i.data["rcode"])
            except KeyError:
                pass
            try:
                if i.data["time_start"]:
                    duration = int(i.data["time_finish"]) - int(i.data["time_start"])
                    hours, remainder = divmod(duration, 3600)
                    minutes, seconds = divmod(remainder, 60) 
                    sys.stdout.write(", Duration: %02d:%02d:%02d (%s - %s)" % (hours, minutes, seconds, misc.md(i.data["time_start"], delim=''), misc.md(i.data["time_finish"], delim='')))
            except KeyError:
                pass
            print
        print
