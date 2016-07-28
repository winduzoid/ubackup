# coding: utf8

import argparse
import os

def readargs():
    parser = argparse.ArgumentParser(description='Ubackup tool is backuping servers through rsync protocol')
    parser.add_argument('host', nargs='*', help='Proceeds custom set of hosts. If omitted, than will backup all set')
    parser.add_argument('-c', '--conf', metavar = 'configfile', help = 'Alternate configuration file. Default is ' + os.path.expanduser('~root') + '/.ubackup/ubackup.conf, /usr/local/etc/ubackup/ubackup.conf, or /etc/ubackup/ubackup.conf')
    parser.add_argument('-r', action='store_const', const=True, help = 'Exclude mode. If set, hosts will be excluded from backup')
    parser.add_argument('-n', action='store_const', const=True, help = 'Do not exec backup process. For example, if you want to make other operations')
    parser.add_argument('-d', action='store_const', const=True, help = 'Dry run mode. Backup will not be produced. Local known_hosts file will be updated')
    parser.add_argument('-s', action='store_const', const=True, help = 'Show configuration')
    parser.add_argument('-l', '--snapshot-list', action='store_const', const=True, help = 'Show list of snapshots')
    parser.add_argument('-v', action='store_const', const=True, help = 'Verbose mode')
    parser.add_argument('--snapshot', nargs='?', const="custom", help = 'Create snapshot by name. If omitted, name will be "custom"')
    parser.add_argument('--snapshot-rotate', action='store_const', const=True, help = 'Rotate snapshots. Remove old snapshots')
    parser.add_argument('--snapshot-rm', nargs='*', metavar = 'snapshot', help = 'Remove snapshot by name. Snapshot list you can see by "-l" option')
    parser.add_argument('--install-config', metavar='path', nargs='?', const=os.path.expanduser('~root') + '/.ubackup', help = 'Install configuration. Default path: ' + os.path.expanduser('~root') + '/.ubackup')
    parser.add_argument('--version', action='store_const', const=True, help = 'Show version')
    return parser.parse_args()
