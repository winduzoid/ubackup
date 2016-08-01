# coding: utf8

import os
import subprocess
import sys
import time
import fcntl

from ubackup.hostinfo import *
from ubackup.misc import *

def gatherHostInfo(host, conf, rcode=None, file_log_rcode = None):

    dir_systeminfo = "/root/system_state"
    hostname = host.conf["hostname"]
    ssh_string = "ssh " + hostname + " "
    if rcode == None:
        str = ssh_string + "mkdir -p /root/system_state"
        subprocess.call(str.split())
        str = ssh_string + "df -h > /root/system_state/df.txt"
        subprocess.call(str.split())
        str = ssh_string + "cat /proc/mounts > /root/system_state/mounts.txt"
        subprocess.call(str.split())
        str = ssh_string + "dpkg -l > /root/system_state/packages.txt"
        subprocess.call(str.split())
        str = ssh_string + "lvscan > /root/system_state/lvscan.txt 2>/dev/null"
        subprocess.call(str.split())
        str = ssh_string + "ifconfig > /root/system_state/ifconfig.txt 2>/dev/null"
        subprocess.call(str.split())
    else:
        str = ssh_string + "echo %d > %s" % (rcode, file_log_rcode)
        subprocess.call(str.split())

def getHosts(conf, debug = None):
    hosts = []
    # get host list
    hosts_lines = os.popen("cat " + conf.conf["file_hosts"] + " | egrep -v '^\s*#' | egrep -v '^$'")
    
    # init host objects
    for i in hosts_lines:
        hosts.append(fillHostInfo(HostConf(i, debug), conf, debug))
    return hosts

def launchRemote(host, filename, log_filename, conf):
    misc = Misc(conf)
    hostname = host.conf["hostname"]
    ssh_string = "ssh " + hostname + " "
    str = "scp -q " + filename + " " + hostname + ":/tmp/ubackup-launch"
    print(misc.md + "Launch script %s... " % stsl(filename))
    logfile = open(log_filename, "a+")
    misc.logDate(logfile)
    logfile.write(stsl("Launch script " + filename + "\n"))
    logfile.close()
    logfile = open(log_filename, "a+")
    subprocess.call(str.split())
    str = ssh_string + "chmod +x /tmp/ubackup-launch; /tmp/ubackup-launch; rm -f /tmp/ubackup-launch"
    subprocess.call(str.split(), stdout=logfile, stderr=logfile)
    logfile.close()
    print(misc.md + "done")
    logfile = open(log_filename, "a+")
    misc.logDate(logfile)
    logfile.write("Done\n")
    logfile.close()

def runBackup(conf, arg, debug = None):
    misc = Misc(conf)
    # if specified "-n", exit
    print "\nBackuping hosts\n"
    hosts = getHosts(conf, debug)
    # if not dry run mode
    if not arg.d:
        # get exclusive lock
        fd = open(conf.conf["file_lock"], "w")
        fcntl.lockf(fd, fcntl.LOCK_EX)

    if not os.path.isdir(conf.conf["dir_backup"]):
        command = "mkdir -p " + conf.conf["dir_backup"]
        subprocess.call(command.split())

    if not os.path.isdir(conf.conf["dir_log"]):
        command = "mkdir -p " + conf.conf["dir_log"]
        subprocess.call(command.split())

    for host in hosts:
        if arg.r:
            # if specified exclude flag, and we have host list, and current host is in this list, do not backup it
            if len(arg.host) > 0 and host.conf["name"] in [x.lower() for x in arg.host]:
                if debug:
                    print "Skipping host %s..." % host.conf["name"]
                continue
            # if specified exclude flag, and we have host list by path, and current host is in this list, do not backup it
            if arg.path and host.conf["dstpath"] in [x.lower() for x in arg.path]:
                if debug:
                    print "Skipping host %s..." % host.conf["name"]
                    print "Host dest path is %s" % host.conf["dstpath"]
                continue
        if not arg.r:
            # if not specified exclude flag, and we have host list, and current host is not in list, do not backup it
            if len(arg.host) > 0 and host.conf["name"] not in [x.lower() for x in arg.host]:
                if debug:
                    print "Skipping host %s..." % host.conf["name"]
                continue
            # if not specified exclude flag, and we have host list by path, and current host is not in list, do not backup it
            if arg.path and host.conf["dstpath"] not in [x.lower() for x in arg.path]:
                if debug:
                    print "Skipping host %s..." % host.conf["name"]
                    print "Host dest path is %s" % host.conf["dstpath"]
                continue
        # print "Backuping host %s...\n" % host.conf["name"]

        try:
            rsync_short_opts = host.conf["rsync_short_opts"]
        except KeyError:
            rsync_short_opts = conf.conf["rsync_short_opts"]

        try:
            rsync_long_opts = host.conf["rsync_long_opts"]
        except KeyError:
            rsync_long_opts = conf.conf["rsync_long_opts"]

        try:
            file_log_rcode = host.conf["file_log_rcode"]
        except KeyError:
            file_log_rcode = conf.conf["file_log_rcode"]

        try:
            str = "egrep -q '^" + host.conf["hostname"] + "\s+.*' /root/.ssh/known_hosts || ssh-keyscan " + host.conf["hostname"] + " >> /root/.ssh/known_hosts"
            subprocess.check_output(str, shell=True)
            str = "rsync " + rsync_short_opts + " " + rsync_long_opts + " --exclude-from " + host.conf["exclude_list"] + " " + host.conf["hostname"] + ":" + host.conf["path"] + " " + host.conf["dst"]            
            print misc.md
            print "Host: " + host.conf["name"]

            if os.path.isfile(conf.conf["dir_custom_config"] + "/" + host.conf["name"]):
                print "Use custom config: " + conf.conf["dir_custom_config"] + "/" + host.conf["name"]

            if host.conf["run_before"]:
                print "Use run_before script: " + stsl(host.conf["run_before"])

            if host.conf["run_after"]:
                print "Use run_after script: " + stsl(host.conf["run_after"])

            print "Destination dir: " + host.conf["dst"]
            print "Log file: " + host.conf["dir_log"] + "/" + host.conf["name"]
            print "Log file rcode: " + file_log_rcode
            print "Use Exclude list: " + host.conf["exclude_list"]
            print "Use command: " + str + "\n"
            # If not in "dry run" mode
            if not arg.d:
                #gatherHostInfo(host)
                # creating log dir if it not exists
                subprocess.call("mkdir -p " + host.conf["dir_log"], shell = True)
                log_filename = host.conf["dir_log"] + "/" + host.conf["name"]

                open(log_filename, "w").close()
                if host.conf["run_before"]:
                    rlcode = launchRemote(host, host.conf["run_before"], log_filename, conf)
                logfile = open(log_filename, "a+")
                misc.logDate(logfile)
                logfile.close()

                logfile = open(log_filename, "a+")
                print(misc.md + "Backuping host... ")
                subprocess.call("mkdir -p " + host.conf["dst"], shell = True)
                rcode = subprocess.call(str.split(), stdout=logfile, stderr=logfile)
                logfile.close()

                gatherHostInfo(host, conf, rcode, file_log_rcode)
                print(misc.md + "Done. Exit code: %d" % rcode)
                logfile = open(log_filename, "a+")
                logfile.write("Exit code: %d\n" % rcode)
                logfile.close()
                if host.conf["run_after"]:
                    rlcode = launchRemote(host, host.conf["run_after"], log_filename, conf)
            print
        except KeyboardInterrupt:
            print "\nKeyboard interrupted"
            sys.exit(1)

    # If not in "dry run" mode
    if not arg.d:
        # unlocking file
        fcntl.lockf(fd, fcntl.LOCK_UN)
        fd.close()
