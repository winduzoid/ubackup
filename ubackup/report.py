# coding: utf8

import sys
import smtplib
from email.mime.text import MIMEText

from cStringIO import StringIO

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
    def __init__(self, conf, arg, debug = None):
        self.arg = arg
        self.conf = conf
        self.debug = debug
        self.reportItem = []
        self.data = {}
    
    def add(self, reportItem):
        self.reportItem.append(reportItem)

    def set(self, name, uvalue):
        self.data[name] = uvalue

    def show(self):
        print "Report\n"
        print self.generate()

    def email(self):
        conf = self.conf
        if self.arg.no_email or self.arg.d:
            return
        elif conf.conf["report_email"].lower() == "false" and not self.arg.email:
            return
        msg = MIMEText(self.generate())
        msg['Subject'] = conf.conf["email_subject"]
        msg['From'] =  conf.conf["email_from"]
        msg['To'] = conf.conf["email_to"]
        s = smtplib.SMTP(conf.conf["email_host"])
        sys.stdout.write("Sending report by email... ")
        sys.stdout.flush()
        try:
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            sys.stdout.write("Done\n")
            sys.stdout.flush()
        except smtplib.SMTPRecipientsRefused:
            print "Incorrect report recipient"

    def generate(self, force = None):
        if force:
            try:
                del(self.genstr)
            except AttributeError:
                pass
        try:
            return self.genstr
        except AttributeError:
            pass
        misc = Misc(self.conf)
        sys.stdout = mystdout = StringIO()
        duration = self.data["TimeFinish"] - self.data["TimeStart"]
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        sys.stdout.write("Duration: %02d:%02d:%02d (%s - %s)\n" % (hours, minutes, seconds, misc.md(self.data["TimeStart"], delim=''), misc.md(self.data["TimeFinish"], delim='')))
        if self.debug:
            for i in sorted(self.data):
                sys.stdout.write("%s: %s\n" % (i, self.data[i]))
        else:
            if self.data["DryRun"] == True:
                sys.stdout.write("DryRun: %s\n" % self.data["DryRun"])
        sys.stdout.write("\nHosts:\n")
        for i in self.reportItem:
            try:
                sys.stdout.write("Code: %d, " % i.data["rcode"])
            except KeyError:
                pass
            sys.stdout.write("Host name = %s" % i.data["name"])
            try:
                if i.data["time_start"]:
                    duration = int(i.data["time_finish"]) - int(i.data["time_start"])
                    hours, remainder = divmod(duration, 3600)
                    minutes, seconds = divmod(remainder, 60) 
                    sys.stdout.write(", Duration: %02d:%02d:%02d (%s - %s)" % (hours, minutes, seconds, misc.md(i.data["time_start"], delim=''), misc.md(i.data["time_finish"], delim='')))
            except KeyError:
                pass
            sys.stdout.write("\n")
        sys.stdout = sys.__stdout__
        return mystdout.getvalue()
