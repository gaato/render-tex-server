#!/usr/local/bin/python

import argparse
import base64
import os
import subprocess
import sys

from PIL import Image, ImageChops


def trim(image_path, range, absolute_trim_width=0):

    image = Image.open(image_path)
    width, _ = image.size
    bg = Image.new('RGB', image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg)
    diff_bbox = diff.convert('RGB').getbbox()
    if absolute_trim_width == 0:
        l = diff_bbox[0] - range
        t = diff_bbox[1] - range
        r = diff_bbox[2] + range
        b = diff_bbox[3] + range
        crop_range = (l, t, r, b)
    elif absolute_trim_width > 0:
        l = absolute_trim_width
        t = diff_bbox[1] - range
        r = width - absolute_trim_width
        b = diff_bbox[3] + range
        crop_range = (l, t, r, b)
    else:
        raise ValueError
    crop_image = image.crop(crop_range)
    crop_image.save('trimed-' + os.path.basename(image_path))


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--plain',
                     help='render without gather environment',
                     action='store_true')
args = parser.parse_args()

stdin = sys.stdin.read()

if args.plain:
    with open('/tex-template/texp.tex', 'r') as f:
        tex_source = f.read()
else:
    with open('/tex-template/tex.tex', 'r') as f:
        tex_source = f.read()

tex_source = tex_source.replace('[REPLACE]', stdin)

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

with open('/tmp/tmp.png', 'wb') as f:
    subprocess.run(['pdftoppm', '-png', '-r', '800', '/tmp/tmp.pdf'], stdout=f)

if args.plain:
    trim('/tmp/tmp.png', 50, 1500)
else:
    trim('/tmp/tmp.png', 50)

with open('trimed-tmp.png' , 'rb') as f:
    result_binary = f.read()

sys.stdout.buffer.write(base64.b64encode(result_binary))
