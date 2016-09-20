# coding: utf8

import argparse
import os


def readargs():
    parser = argparse.ArgumentParser(
        description='Ubackup tool is backuping servers through rsync protocol')
    parser.add_argument(
        'host', nargs='*', help='Proceeds custom set of hosts. If omitted, than will backup all set')
    parser.add_argument('-c', '--conf', metavar='configfile', help='Alternate configuration file. Default is ' +
                        os.path.expanduser('~root') + '/.ubackup/ubackup.conf, /usr/local/etc/ubackup/ubackup.conf, or /etc/ubackup/ubackup.conf')
    parser.add_argument('-p', '--path', nargs='*',
                        help='Backup only hosts which have destination path specified in this option. It can be used with "-r" option')
    parser.add_argument('-r', action='store_const', const=True,
                        help='Exclude mode. If set, hosts will be excluded from backup')
    parser.add_argument('-n', action='store_const', const=True,
                        help='Do not exec backup process. For example, if you want to make other operations')
    parser.add_argument('-d', action='store_const', const=True,
                        help='Dry run mode. Backup will not be produced. Local known_hosts file will be updated')
    parser.add_argument('-s', action='store_const',
                        const=True, help='Show configuration')
    parser.add_argument('-l', '--snapshot-list', action='store_const',
                        const=True, help='Show list of snapshots')
    parser.add_argument('-v', action='store_const',
                        const=True, help='Verbose mode')
    parser.add_argument('--snapshot', metavar='LABEL', nargs='?', const="custom",
                        help='Create snapshot by label. If omitted, label will be "custom"')
    parser.add_argument('--snapshot-volume', metavar='VOLUME',
                        nargs='*', help='Create snapshot only on specified volumes')
    parser.add_argument('--snapshot-rotate', action='store_const',
                        const=True, help='Rotate snapshots. Remove old snapshots')
    parser.add_argument('--snapshot-rm', nargs='*', metavar='SNAPSHOT',
                        help='Remove snapshot by name. Snapshot list you can see by "-l" option')
    parser.add_argument('--email', action='store_const',
                        const=True, help="Send report by email")
    parser.add_argument('--no-email', action='store_const',
                        const=True, help="Don't send report by email")
    parser.add_argument('--version', action='store_const',
                        const=True, help='Show version')
    return parser.parse_args()


def readargsInstall():
    parser = argparse.ArgumentParser(
        description='ubackup-install tool is installing ubackup')
    parser.add_argument('install_config', metavar='path', nargs='?',
                        help='path to directory contains config file ubackup.conf')
    return parser.parse_args()
