#!/usr/local/bin/python

import base64
import os
import subprocess
import sys

tex_source = sys.stdin.read()

with open('/tmp/tmp.tex', 'w') as f:
    f.write(tex_source)

try:
    uplatex = subprocess.run(['uplatex', '-halt-on-error', '-output-directory=/tmp', '/tmp/tmp.tex'], stdout=subprocess.PIPE, timeout=10.0)
except subprocess.TimeoutExpired:
    exit(2)

if uplatex.returncode != 0:
    with open('/tmp/tmp.log', 'r') as f:
        error = '!' + f.read().split('!')[1].split('Here')[0]
    print(error)
    exit(1)

try:
    subprocess.run(['dvipdfmx', '-q','-o', '/tmp/tmp.pdf', '/tmp/tmp.dvi'], timeout=10.0)
except subprocess.TimeoutExpired:
    exit(2)

with open('/tmp/tmp.pdf', 'rb') as f:
    result_binary = f.read()

sys.stdout.buffer.write(base64.b64encode(result_binary))
