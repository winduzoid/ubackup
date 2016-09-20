# coding: utf8

import os
import re
import subprocess
import time

from ubackup.conf import *

# Host object


class HostConf:

    def __init__(self, conf, host_line, debug=None):

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
        except IndexError:
            dst_path = conf.conf["dir_default_dest"]

        self.conf["dstpath"] = dst_path
        self.conf["group_name"] = dst_path.replace("/", "-")

        if dst_path == "/":
            self.conf["dst"] = None
            self.conf["dir_log"] = None
            self.conf["dstpath"] = None
            self.conf["group_name"] = ""
        elif re.match(".*/$", dst_path):
            self.conf["dst"] = dst_path
            self.conf["dir_log"] = os.path.dirname(
                re.sub(r'(.*)/$', r'\1', dst_path))
            self.conf["group_name"] = ""
        else:
            self.conf["dst"] = dst_path + "/" + self.conf["name"]
            self.conf["dir_log"] = dst_path

        if debug:
            print "destination path = %s, dir_log = %s, group_name = %s" % (self.conf["dst"], self.conf["dir_log"], self.conf["group_name"])


def fillHostInfo(hostconf, conf, debug=None):

    if debug:
        print hostconf.conf

    exclude_list = conf.conf["dir_exclude"] + "/" + hostconf.conf["name"]
    custom_config = conf.conf["dir_custom_config"] + \
        "/" + hostconf.conf["name"]
    run_before = conf.conf["dir_run_after"] + "/" + hostconf.conf["name"]
    run_after = conf.conf["dir_run_after"] + "/" + hostconf.conf["name"]
    custom_group_config = ""
    exclude_group_list = ""
    run_group_before = ""
    run_group_after = ""
    if hostconf.conf["group_name"]:
        custom_group_config = conf.conf[
            "dir_custom_config"] + "/GROUP." + hostconf.conf["group_name"]
        exclude_group_list = conf.conf[
            "dir_exclude"] + "/GROUP." + hostconf.conf["group_name"]
        run_group_before = conf.conf[
            "dir_run_before"] + "/GROUP." + hostconf.conf["group_name"]
        run_group_after = conf.conf["dir_run_after"] + \
            "/GROUP." + hostconf.conf["group_name"]

    if os.path.isfile(exclude_list):
        hostconf.conf["exclude_list"] = exclude_list
    elif os.path.isfile(exclude_group_list):
        hostconf.conf["exclude_list"] = exclude_group_list
    else:
        hostconf.conf["exclude_list"] = conf.conf["dir_exclude"] + "/default"

    if os.path.isfile(custom_config):
        crc = ReadConf(custom_config)
        cconf = ItemConfig(crc, "custom")
        hostconf.conf.update(cconf.conf)
    elif custom_group_config:
        if os.path.isfile(custom_group_config):
            crc = ReadConf(custom_group_config)
            cconf = ItemConfig(crc, "custom")
            hostconf.conf.update(cconf.conf)

    # destination dir
    if hostconf.conf["dst"]:
        hostconf.conf["dst"] = conf.conf[
            "dir_backup"] + "/" + hostconf.conf["dst"]
    else:
        hostconf.conf["dst"] = conf.conf[
            "dir_backup"] + "/" + hostconf.conf["name"]

    # dir log
    if hostconf.conf["dir_log"]:
        hostconf.conf["dir_log"] = conf.conf["dir_backup"] + "/" + \
            hostconf.conf["dir_log"] + "/" + conf.conf["dir_log_name"]
    else:
        hostconf.conf["dir_log"] = conf.conf["dir_log"] + "/" + conf.conf["dir_log_name"]

    if debug:
        print "Dir log: %s" % hostconf.conf["dir_log"]

    # src path
    if not hostconf.conf["path"]:
        hostconf.conf["path"] = "/"

    # run scripts

    # run_before
    if os.path.isfile(run_before):
        hostconf.conf["run_before"] = run_before
    elif os.path.isfile(run_group_before):
        hostconf.conf["run_before"] = run_group_before
    elif os.path.isfile(conf.conf["dir_run_before"] + "/default"):
        hostconf.conf["run_before"] = conf.conf["dir_run_before"] + "/default"
    else:
        hostconf.conf["run_before"] = None

    # run after
    if os.path.isfile(run_after):
        hostconf.conf["run_after"] = run_after
    elif os.path.isfile(run_group_after):
        hostconf.conf["run_after"] = run_group_after
    elif os.path.isfile(conf.conf["dir_run_after"] + "/default"):
        hostconf.conf["run_after"] = conf.conf["dir_run_after"] + "/default"
    else:
        hostconf.conf["run_after"] = None

    if debug:
        print hostconf.conf

    return hostconf
