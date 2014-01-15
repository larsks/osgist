#!/usr/bin/python

import os
import sys
import argparse
import json
import subprocess
import gist

def parse_args():
    p = argparse.ArgumentParser()
    return p.parse_args()

def create(data):
    p = subprocess.Popen(['curl', '-d', '@-', '-sf', gist.gist_url],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)

    stdout, stderr = p.communicate(data)
    res = json.loads(stdout)
    return res

def main():
    args = parse_args()
    res = create(sys.stdin.read())
    print res['html_url']

if __name__ == '__main__':
    main()

