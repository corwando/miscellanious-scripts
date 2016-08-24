import os, sys, getopt
import argparse, subprocess
import shutil

__author__ = 'Teijo K-K'


# Get filename to process from command line argument
parser = argparse.ArgumentParser(description='Get filename for image to process')
parser.add_argument('-i','--input', help='Input file name',required=True)
args = parser.parse_args()


# Take a copy of original file 
# To-do:
# - support for multiple image file formats. Remember to modify also convert command in below for loop.
shutil.copyfile(args.input, '000.png')


# Use ImageMagick's identify command to determine width of given image
width = subprocess.check_output('identify -ping -format %w {}'.format(args.input))


# Store width as an integer
a = int(width.decode(sys.stdout.encoding))


# Use ImageMagick's convert tool to roll given image by one pixel and
# store it as new file
for i in range(0,a-1):
	subprocess.call('convert -roll +1 {0:03d}.png {1:03d}.png' .format(i, i+1), shell=True)

	
# Create animation from sequence of images
# scale argument is used as workaround if source images' width is not divideable by 2
# which is a requirement of ffmpeg
#
# To-do:
# - make framerate adjustable or selectable between 25 and 30
subprocess.call('ffmpeg -framerate 25 -i %03d.png -c:v libx264 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,fps=25,format=yuv420p" out.mp4', shell=True)