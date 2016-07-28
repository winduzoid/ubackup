# coding: utf8

import sys
import os
import subprocess
import shutil

from lib.misc import *

from ConfigParser import SafeConfigParser

# Simple class for reading configuration
class ReadConf:

    def __init__(self, configFilePath, debug):
        self.cp = SafeConfigParser()
        self.section = "default"
        #if os.path.isfile
        homedir = os.path.expanduser('~root')
        conffile = ""
        if configFilePath:
            conffile = configFilePath
        elif os.path.isfile(homedir + "/.ubackup/ubackup.conf"):
            conffile = homedir + "/.ubackup/ubackup.conf"
        elif os.path.isfile("/usr/local/etc/ubackup/ubackup.conf"):
            conffile = "/usr/local/etc/ubackup/ubackup.conf"
        elif os.path.isfile("/etc/ubackup/ubackup.conf"):
            conffile = "/etc/ubackup/ubackup.conf"
        if debug:
            print "configpath: %s" % conffile
        self.cp.read(conffile)

    def items(self,section=None):
        if section == None: section = self.section
        return self.cp.items(section)

    def rc(self,keyname,section=None):
        if section == None: section = self.section
        return self.cp.get(section,keyname)

# Object with config
class ItemConfig:

    def __init__(self,readConf, section = "default"):
        self.conf = {}
        self.snap_disable = []
        self.snapshot_names = []

        try:
            for i in readConf.cp.items(section):
                self.conf[i[0]] = i[1]
        except:
            print "Problem with config"
            sys.exit(1)

        # Init absent configuration options
        self.fillMissingConf()

        try:
            for i in [x.strip() for x in self.conf["snapshot_disable"].split(',')]:
                self.snap_disable.append(i)
        except KeyError:
            del self.snap_disable

        try:
            for i in [x.strip() for x in self.conf["snapshot_names"].split(',')]:
                self.snapshot_names.append(i.split(":"))
        except KeyError:
            del self.snapshots

    def fillMissingConf(self):
        dconf = {}

        try:
            dconf["dir_etc"] = self.conf["dir_etc"]
        except KeyError:
            dconf["dir_etc"] = "/root/.ubackup/"

        try:
            dconf["dir_backup"] = self.conf["dir_backup"]
        except KeyError:
            dconf["dir_backup"] = "/data/backup/"

        dconf["dir_log"] = dconf["dir_backup"] + "/LOG"
        dconf["file_lock"] = "/tmp/ubackup.lock"
        dconf["file_hosts"] = dconf["dir_etc"] + "/hosts.conf"
        dconf["dir_exclude"] = dconf["dir_etc"] + "/excludes/"
        dconf["dir_custom_config"] = dconf["dir_etc"] + "/custom_config/"
        dconf["dir_custom"] = dconf["dir_etc"] + "/custom/"
        dconf["dir_exec"] = dconf["dir_etc"] + "/exec/"
        dconf["dir_run_before"] = dconf["dir_etc"] + "/run_before/"
        dconf["dir_run_after"] = dconf["dir_etc"] + "/run_after/"
        dconf["zpool"] = "data"
        dconf["snapshot_disable"] = "data/backup, data/archive"
        dconf["snapshot_prefix"] = "ubackup"
        dconf["rsync_short_opts"] = "-aHAXv"
        dconf["rsync_long_opts"] = "--delete --numeric-ids --delete-excluded"
        dconf["snapshot_names"] = "daily:7, weekly:4, monthly:4"
        dconf["date_format"] = "%Y.%m.%d %H:%M:%S"

        for i in dconf:
            try:
                self.conf[i] = stsl(self.conf[i])
            except KeyError:
                self.conf[i] = stsl(dconf[i])

def showConfig(conf,arg):
    for i in sorted(conf.conf):
        print "%s = %s" % (i, conf.conf[i])

    print "\nCalculated values:"
    print "snap_disable: %s" % conf.snap_disable
    print "snapshot_names: %s" % conf.snapshot_names
    sys.exit(0)

def installConfig(arg):
    if arg.install_config:

        homedir = os.path.expanduser('~root')
        ssh_config = homedir + '/.ssh/config'
        config_dir = arg.install_config + "/"
        src_dir = sys.path[0]

        if os.path.isfile(ssh_config):
            subprocess.call('sed -i "/^\s*HashKnownHosts/d" ' + ssh_config, shell=True)
        subprocess.call('echo "HashKnownHosts no" >> ' + ssh_config, shell=True)
        try:
            print "Installing config files to %s" % config_dir
            shutil.copytree(src_dir + '/etc/ubackup', config_dir)
            str = 'sed -i "s|^\s*dir_etc\s*=.*|dir_etc = ' + config_dir + '|g" ' + config_dir + '/ubackup.conf'
            subprocess.call(str, shell=True)
        except OSError:
            print "Problem during installation. Keep in mind that destination directory must not be exist"

        sys.exit(0)
