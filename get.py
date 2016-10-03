#!/bin/python3

import argparse
import sys, os
import subprocess
import shutil
import urllib.request
from zipfile import ZipFile
import re

parser = argparse.ArgumentParser(description='Set up a Kattis skeleton')
parser.add_argument('name', help='the name of the problem')
args = parser.parse_args()

subprocess.check_call([shutil.which("curl"), "-o", "samples.zip", "https://open.kattis.com/problems/" + args.name + "/file/statement/samples.zip"])

os.mkdir(args.name)
os.mkdir(args.name + "/src")
os.mkdir(args.name + "/samples")

shutil.copy("_skeleton/src/_skeleton.cpp", args.name + "/src/" + args.name + ".cpp")

if os.path.isfile("samples.zip"):
	with ZipFile("samples.zip") as f:
		inre = re.compile(r'[a-zA-Z0-9_\.\-]*\.in', re.IGNORECASE)
		ansre = re.compile(r'[a-zA-Z0-9_\.\-]*\.ans', re.IGNORECASE)
		infiles = []
		ansfiles = []
		for name in f.namelist():
			match = inre.fullmatch(name)
			if match:
				infiles.append(name)
				continue
			match = ansre.fullmatch(name)
			if match:
				ansfiles.append(name)
				continue
			print("ERROR: samples.zip contains the weird file \"", name, "\"", sep='')
			sys.exit(1)
		if len(infiles) != len(ansfiles):
			print("ERROR: Number of input files (", len(infiles), ") is not equal to the number of answer files (", len(ansfiles), ")", sep='')
			sys.exit(1)
		infiles.sort()
		ansfiles.sort()
		sampleid = 0
		for t in zip(infiles, ansfiles):
			sampleid += 1
			if t[0][:-3] != t[1][:-4]:
				print("ERROR: Name of input file (", t[0], ") does not match name of answer file (", t[1], ")", sep='')
				sys.exit(1)
			with f.open(t[0]) as infile, open(args.name + "/samples/" + args.name + "-" + str(sampleid) + ".in", 'bx') as outfile:
				shutil.copyfileobj(infile, outfile)
			with f.open(t[1]) as infile, open(args.name + "/samples/" + args.name + "-" + str(sampleid) + ".ans", 'bx') as outfile:
				shutil.copyfileobj(infile, outfile)

os.remove("samples.zip")