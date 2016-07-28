# ubackup

Backup system based on rsync and ZFS

It uses rsync for synchronization and zfs filesystem for snapshoting.
A feature of the application is that it actually makes clones of hosts.

## Requirements

* python 2.x
* zfs
* rsync
* sed

The app has been tested on Ubuntu 14.04, but it should work on any Linux distro that supports zfs. Also it will be tested on FreeBSD soon.

## Installation

Clone or download to any directory and run *ubackup --install-config*. By default config files will be installed to $HOME/.ubackup.
You can install files to another location by specified path in the --install-config option.

## Configuration

Section in the filling state

### hosts.conf

File contains hosts backup rules, one host on the line. Each host consists of four parameters delimetered by space symbol. First parameter (host address) is necessary, and three other is not.
Parameters:

* host address. May be in FQDN form, or just ip address
* destination path. If path ending with slash than destination path will looks like **dir**. If path not ending with slash, than destination path will looks like **dir/hostname**
* host alias. If omitted, than the host name will be taken from the host address (first parameter)
* source dir. By default is "/", than copying all filesystem of source host.
