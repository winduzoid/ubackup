# ubackup

Backup system based on rsync and ZFS

It uses rsync for synchronization and zfs filesystem for snapshoting

## Requirements

* python 2.x
* zfs
* rsync
* sed

The app has been tested on Ubuntu 14.04, but it should work on any Linux distro that supports zfs. Also it will be tested on FreeBSD soon.

## Installation

Clone to any directory and run *ubackup --install-config*. By default config files will be installed to $HOME/.ubackup.
You can install files to another location by specified path in the --install-config option.
