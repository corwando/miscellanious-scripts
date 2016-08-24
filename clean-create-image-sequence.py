import os, sys, getopt
import argparse, subprocess
import shutil

__author__ = 'Teijo K-K'


parser = argparse.ArgumentParser(description='Get filename for image to process')
parser.add_argument('-i','--input', help='Input file name',required=True)
args = parser.parse_args()
shutil.copyfile(args.input, '000.png')
width = subprocess.check_output('identify -ping -format %w {}'.format(args.input))
a = int(width.decode(sys.stdout.encoding))

"""
for i in range(0,a-1):
	subprocess.call('convert -roll +1 {0:03d}.png {1:03d}.png' .format(i, i+1), shell=True)
"""

subprocess.call('ffmpeg -framerate 25 -i %03d.png -c:v libx264 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,fps=25,format=yuv420p" out.mp4', shell=True)