# coding: utf8

import os
import re
import subprocess
import time

from ubackup.conf import *

# Host object
class HostConf:

    def __init__(self, host_line, debug = None):

        hostsplit = host_line.split()
        self.conf = {}

        try:
            self.conf["hostname"] = hostsplit[0].lower()
            self.conf["name"] = self.conf["hostname"]
        except IndexError:
            self.conf["hostname"] = None

        try:
            self.conf["path"] = hostsplit[3]
        except IndexError:
            self.conf["path"] = None

        try:
            self.conf["alias"] = hostsplit[2].lower()
            self.conf["name"] = self.conf["alias"]
        except IndexError:
            self.conf["alias"] = None

        try:
            dst_path = hostsplit[1]
            if dst_path == "/":
                self.conf["dst"] = None
                self.conf["dir_log"] = None
            elif re.match(".*/$", dst_path):
                self.conf["dst"] = dst_path
                self.conf["dir_log"] = os.path.dirname(re.sub(r'(.*)/$', r'\1', dst_path))
            else:
                self.conf["dst"] = dst_path + "/" + self.conf["name"]
                self.conf["dir_log"] = dst_path
        except IndexError:
            self.conf["dst"] = None
            self.conf["dir_log"] = None

        if debug:
            print "destination path = %s, dir_log = %s" % (self.conf["dst"], self.conf["dir_log"])

def fillHostInfo(hostconf, conf, debug = None):

    # exclude list
    exclude_list = conf.conf["dir_exclude"] + "/" + hostconf.conf["name"]

    if os.path.isfile(exclude_list):
        hostconf.conf["exclude_list"] = exclude_list
    else:
        hostconf.conf["exclude_list"] = conf.conf["dir_exclude"] + "/default"

    # custom config
    custom_config = conf.conf["dir_custom_config"] + "/" + hostconf.conf["name"]

    if os.path.isfile(custom_config):
        crc = ReadConf(custom_config)
        cconf = ItemConfig(crc)
        hostconf.conf.update(cconf.conf)

    # destination dir
    if hostconf.conf["dst"]:
        hostconf.conf["dst"] = conf.conf["dir_backup"] + "/" + hostconf.conf["dst"]
    else:
        hostconf.conf["dst"] = conf.conf["dir_backup"] + "/" + hostconf.conf["name"]

    # dir log
    if hostconf.conf["dir_log"]:
        hostconf.conf["dir_log"] = conf.conf["dir_backup"] + "/" + hostconf.conf["dir_log"] + "/" + conf.conf["dir_log_name"]
    else:
        hostconf.conf["dir_log"] = conf.conf["dir_log"] + "/" + conf.conf["dir_log_name"]

    if debug:
        print "Dir log: %s" % hostconf.conf["dir_log"]

    # src path
    if not hostconf.conf["path"]:
        hostconf.conf["path"] = "/"

    # run scripts

    # run_before
    if os.path.isfile(conf.conf["dir_run_before"] + "/" + hostconf.conf["name"]):
        hostconf.conf["run_before"] = conf.conf["dir_run_before"] + "/" + hostconf.conf["name"]
    elif os.path.isfile(conf.conf["dir_run_before"] + "/default"):
        hostconf.conf["run_before"] = conf.conf["dir_run_before"] + "/default"
    else:
        hostconf.conf["run_before"] = None

    # run after
    if os.path.isfile(conf.conf["dir_run_after"] + "/" + hostconf.conf["name"]):
        hostconf.conf["run_after"] = conf.conf["dir_run_after"] + "/" + hostconf.conf["name"]
    elif os.path.isfile(conf.conf["dir_run_after"] + "/default"):
        hostconf.conf["run_after"] = conf.conf["dir_run_after"] + "/default"
    else:
        hostconf.conf["run_after"] = None

    return hostconf

