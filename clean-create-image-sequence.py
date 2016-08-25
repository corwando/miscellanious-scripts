import os, sys, getopt
import argparse, subprocess
import shutil

__author__ = 'Teijo K-K'


# Get filename to process from command line argument
parser = argparse.ArgumentParser(
	description='Creates roll animation for given static image. ImageMagick and ffmpeg are required.'
	' Supported file formats are: png, jpg and bmp. Resulting file is <input-file-name>.mp4',
	epilog="Example: \nclean-create-image-sequence.py -i small.png -f 25")
parser.add_argument('-i','--input', help='Input file name',required=True)
parser.add_argument('-f','--frame-rate', type=int, default=25, help='Animation frame rate. Typically 25 fps or 30 fps.',required=False)
args = parser.parse_args()


# Store given filename and file extension to variables for later usage
file_extension = os.path.splitext(args.input)[1]
file_base = os.path.splitext(args.input)[0]


# Accept only png bmp and jpg file formats.
# Abort if invalid file format was provided
if file_extension == ".png" or file_extension == ".jpg" or file_extension == ".bmp":
	print ("File format is:", os.path.splitext(args.input)[1])
else:
	print ("\nInvalid file format.\nOnly .png .jpg and .bmp formats are supported.\n\nAborting...")
	os._exit(1)
	

# Take a copy of original file 
copiedFile = '000%s' % file_extension
shutil.copyfile(args.input, copiedFile)


# Use ImageMagick's identify command to determine width of given image
width = subprocess.check_output('identify -ping -format %w {}'.format(args.input))

# Store width as an integer to variable a
a = int(width.decode(sys.stdout.encoding))


# Use ImageMagick's convert tool to roll given image by one pixel and store it as new file
for i in range(0,a-1):
	subprocess.call('convert -roll +1 {0:03d}.png {1:03d}.png' .format(i, i+1), shell=True)


# Create animation from sequence of images
# "scale" argument is used as workaround if source images' width is not divideable by 2 which is a requirement of ffmpeg

# To-do:
# - make framerate adjustable or selectable between 25 and 30
subprocess.call('ffmpeg -framerate 25 -i %03d.png -c:v libx264 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,fps=25,format=yuv420p" out.mp4', shell=True)
