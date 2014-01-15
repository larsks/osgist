#!/usr/bin/python
#
# This script will run several neutron list- and show- commands and 
# post them to gist.github.com.

import os
import sys
import argparse
import subprocess
import shlex
import logging

import gist

def run(command):
    logging.info('running: %s', command)
    p = subprocess.Popen(shlex.split(command),
                         stdout=subprocess.PIPE)
    stdout,stderr = p.communicate()
    return stdout

def ns_run(ns, command):
    if ns == 'global':
        return run(command)
    else:
        return run('ip netns exec %s ' % ns + command)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--verbose', '-v', action='store_true')
    p.add_argument('--description', '-d',
                   default='Network configuration information')
    return p.parse_args()

def main():
    args = parse_args()
    if args.verbose:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARN

    logging.basicConfig(level=loglevel)
    logging.warn('collecting network configuration information')
    logging.warn('run with --verbose to see command execution')

    g = gist.Gist(args.description)

    g.add('ovs-vsctl-show.txt',       run('ovs-vsctl show'))

    for ns in [ 'global' ] + run('ip netns').split('\n'):
        if not ns:
            continue

        data = [
            '# ip addr show',
            ns_run(ns, 'ip addr'),
            '# ip route',
            ns_run(ns, 'ip route'),
            '# iptables-save',
            ns_run(ns, 'iptables-save')
        ]

        g.add(ns, '\n'.join(data))

    readme = '''
    # Network configuration dump

    This is an automatically generated configuration dump
    containing the following files:

    '''

    readme = '\n'.join(x[4:] for x in readme.split('\n'))
    contents = '\n'.join('- [%s](#%s)' % (x,gist.anchor(x)) for x in g.filenames())

    g.add('00README.md', readme+contents)
    print g.to_json()

if __name__ == '__main__':
    main()

