#!/usr/bin/env python3
import argparse
import os
import re
import sys
import tarfile
import shutil
import subprocess

FILES = ['wc209.c', 'dfa.pdf', 'readme', 'EthicsOath.pdf']

def fatal(msg):
    print(f'[-] ERROR: {msg}')
    sys.exit(1)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('tar', help='a tar.gz file to check before submission')
    return p.parse_args()

def get_student_id():
    student_id = os.path.join(os.path.dirname(__file__), '../STUDENT_ID')
    if not os.path.exists(student_id):
        fatal('Cannot find STUDENT_ID')

    return open(student_id).read().strip()

if __name__ == '__main__':
    tar = parse_args().tar

    # General check
    if not os.path.exists(tar):
        fatal(f'{tar} does not exist')

    sid = get_student_id()

    expected_filename = f'{sid}_assign1.tar.gz'
    if os.path.basename(tar) != expected_filename:
        fatal(f'A file name is wrong (expected: {expected_filename})')
        sys.exit(1)

    if not tarfile.is_tarfile(tar):
        fatal('Not a tar file')
        sys.exit(1)

    # Check a tar.gz satisifes requirements
    tar = tarfile.open(tar)

    files = set(FILES)
    for f in tar:
        name = f.name
        if not name in files:
            fatal(f'{name} is incorrectly included')

        files.remove(name)

    if files:
        for name in files:
            fatal(f'{name} should be included')

    # Check whether wc209.c can be compiled with gcc209
    if not shutil.which('gcc209'):
        fatal('Cannot find gcc209')

    with open('.wc209.c', 'wb') as f:
        f.write(tar.extractfile('wc209.c').read())

    p = subprocess.run(['gcc209', '-o', '.wc209', '.wc209.c'])

    if p.returncode != 0:
        fatal('Cannot be compiled with gcc209')

    print('[+] Good to submit :)')