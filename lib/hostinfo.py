# coding: utf8

import os
import subprocess
import time

from lib.conf import *

# класс с конфигурацией хоста
class HostConf:

    def __init__(self,host_line):

        hostsplit = host_line.split()
        self.conf = {}

        try:
            self.conf["hostname"] = hostsplit[0].lower()
            self.conf["name"] = self.conf["hostname"]
        except IndexError:
            self.conf["hostname"] = None

        try:
            self.conf["path"] = hostsplit[2]
        except IndexError:
            self.conf["path"] = None

        try:
            self.conf["dst"] = hostsplit[1]
        except IndexError:
            self.conf["dst"] = None

        try:
            self.conf["alias"] = hostsplit[3].lower()
            self.conf["name"] = self.conf["alias"]
        except IndexError:
            self.conf["alias"] = None

def fillHostInfo(hostconf, conf):

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
        hostconf.conf["run_before"] = Non

    # run after
    if os.path.isfile(conf.conf["dir_run_after"] + "/" + hostconf.conf["name"]):
        hostconf.conf["run_after"] = conf.conf["dir_run_after"] + "/" + hostconf.conf["name"]
    elif os.path.isfile(conf.conf["dir_run_after"] + "/default"):
        hostconf.conf["run_after"] = conf.conf["dir_run_after"] + "/default"
    else:
        hostconf.conf["run_after"] = None

    return hostconf

