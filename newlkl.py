#!/usr/bin/env python

"""
Author: Ivan Debono 2019
Creates a new likelihood from an existing likelihood in MontePython/montepython/likelihoods

Usage:
python newlkl.py old new path
"""
import errno
import os
import argparse
import shutil
import fileinput
import sys

parser = argparse.ArgumentParser()
parser.add_argument("src", help="Original likelihood name",type=str)
parser.add_argument("dest", help="New likelihood name",type=str)
parser.add_argument("path", help="Path to likelihood folder",type=str)
args = parser.parse_args()


src=str(args.src)
dest=str(args.dest)
path=str(args.path)

print("Path:",path)
print("Old likelihood:",src)
print("New likelihood:",dest)


# Copy the existing likelihood folder and its files with new name. 
try:
    shutil.copytree(os.path.join(path,src), os.path.join(path,dest))
except OSError as e:
    # If the error was caused because the source wasn't a directory
    if e.errno == errno.ENOTDIR:
        shutil.copy(os.path.join(path,src), os.path.join(path,dest))
    else:
        print('Directory not copied. Error: %s' % e)


datafile=os.path.join(path,dest,dest+'.data')
initfile=os.path.join(path,dest,'__init__.py')

# Modify name of .data file
try:
    os.rename(os.path.join(path,dest,src+'.data'),datafile)
except:
    print("ERROR! Likelihood already exists")
    sys.exit(1)

# Modify the copied .data file
# This part may be modified by user according to requirements
for line in fileinput.input(datafile, inplace=1):
    if src+"." in line:
        line = line.replace(src+".", dest+".")
    if src+'_fiducial.dat' in line:
        line = line.replace(src+'_fiducial.dat', dest+'_fiducial.dat') 
    sys.stdout.write(line)

# Modify the copied __init__.py file
for line in fileinput.input(initfile, inplace=1):
    if line.strip().startswith('class'):
        line = line.replace(src, dest)
    sys.stdout.write(line)

print("Created new likelihood:", dest)


