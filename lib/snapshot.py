# coding: utf8

import time
import os
import re
import subprocess
import sys

def createSnapshot(conf, arg, debug = None):
#    print mydate + "\n"
    if not arg.snapshot:
        return
    print "\nCreating snapshot\n"
    snapshot_prefix = conf.conf["snapshot_prefix"] + "_" + arg.snapshot + "_"

    volumes = os.popen("/sbin/zfs list | grep -v NAME | egrep '^" + conf.conf["zpool"] + "' | awk '{print $1}'")
    #volumes = subprocess.check_output("/sbin/zfs list | grep -v NAME | egrep '^" + conf.conf["zpool"] + "' | awk '{print $1}'")
    for volume in volumes:
        volume = volume.strip("\n")
        if volume in [x.strip() for x in conf.conf["snapshot_disable"].split(',')]:
            if debug:
                print "Snapshot of volume %s is disabled" % volume
            continue
        snaptime = time.strftime("%Y-%m-%d-%H:%M:%S")
        if not arg.d:
            print "Creating snapshot: " + volume + "@" + snapshot_prefix + snaptime
            str = "/sbin/zfs snapshot " + volume + "@" + snapshot_prefix + snaptime
            subprocess.call(str.split())
        else:
            print "Would create snapshot: " + volume + "@" + snapshot_prefix + snaptime

def delSnap(SnapshotName):
    str = "/sbin/zfs destroy " + SnapshotName
    subprocess.call(str.split())

# creating snapshot names for deletion
def rotateSnapshot(conf, arg):
    if not arg.snapshot_rotate:
        return
    print "\nRotating snapshots"
    # get pool list
    volumes = os.popen("/sbin/zfs list | grep -v NAME | egrep '^" + conf.conf["zpool"] + "' | awk '{print $1}'")
    # loop on pool list
    for volume in volumes:
        volume = volume.strip("\n")
        # get mount point for the current volume
        dir_volume = subprocess.check_output("/sbin/zfs list " + volume + " | grep -v NAME | awk '{print $5}'", shell=True).strip("\n")
        # get sorted snapshot list for the current volume
        snaplist = sorted(os.listdir(dir_volume + "/.zfs/snapshot"), reverse=True)
        # loop on snapshot type list
        for i in conf.snapshot_names:
            # get snapshot list for current type
            fsnaplist = filter(lambda x:re.search(r'^' + conf.conf["snapshot_prefix"] + "_" +  i[0], x), snaplist)
            # loop on this list
            for j in fsnaplist:
                ee = int(i[1])
                if j not in fsnaplist[0:ee]:
                    snapname = volume + "@" + j
                    print "Removing snapshot: %s" % snapname
                    if not arg.d:
                        delSnap(snapname)

def snapshotList(arg):
    if not arg.snapshot_list:
        return
    str = "zfs list -t snapshot,filesystem -o space"
    subprocess.call(str.split())
    sys.exit(0)

def snapshotRm(arg):
    if not arg.snapshot_rm:
        return
    for i in arg.snapshot_rm:
        if re.match('.*@.*', i):
            print "Removing snapshot: %s" % i
            if not arg.d:
                delSnap(i)
    sys.exit(0)
