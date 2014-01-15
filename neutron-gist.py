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

def neutron_list(command):
        p = subprocess.Popen(['neutron'] + shlex.split(command),
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return [x.strip() for x in stdout.strip().split('\n')[1:]]

def run(command):
    logging.info('running: %s', command)
    p = subprocess.Popen(shlex.split(command),
                         stdout=subprocess.PIPE)
    stdout,stderr = p.communicate()
    return stdout

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
    logging.warn('collecting neutron configuration information')
    logging.warn('run with --verbose to see command execution')

    g = gist.Gist(args.description)

    g.add('net-list.txt',       run('neutron net-list'))
    g.add('subnet-list.txt',    run('neutron subnet-list'))
    g.add('router-list.txt',    run('neutron router-list'))
    g.add('port-list.txt',      run('neutron port-list'))

    for net in neutron_list('net-list -Fid -fcsv --quote none'):
        g.add('net-%s.txt' % net, run('neutron net-show %s' % net))
    for subnet in neutron_list('subnet-list -Fid -fcsv --quote none'):
        g.add('subnet-%s.txt' % subnet, run('neutron subnet-show %s' % subnet))
    for router in neutron_list('router-list -Fid -fcsv --quote none'):
        g.add('router-%s.txt' % router, run('neutron router-show %s' % router))


    readme = '''
    # Neutron configuration dump

    This is an automatically generated configuration dump
    containing the following files:

    '''

    readme = '\n'.join(x[4:] for x in readme.split('\n'))
    contents = '\n'.join('- [%s](#%s)' % (x,gist.anchor(x)) for x in g.filenames())

    g.add('00README.md', readme+contents)
    print g.to_json()

if __name__ == '__main__':
    main()

