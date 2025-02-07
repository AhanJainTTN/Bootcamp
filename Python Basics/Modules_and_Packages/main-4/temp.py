import os
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-name")
parser.add_argument("-type")
parser.add_argument("-maxdepth", type=int)
parser.add_argument("-atime", type=int)
parser.add_argument("directory", type=str)
args = parser.parse_args()

dir = args.directory
name = args.name
depth = args.maxdepth
type = args.type
atime = args.atime

print(name, depth, type, atime, dir)

print(os.listdir(dir))
