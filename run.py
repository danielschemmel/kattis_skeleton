#!/bin/python3

import sys
import argparse
import glob
import subprocess
import shutil
import submit
import os
import re

parser = argparse.ArgumentParser(description='Set up a Kattis skeleton')
parser.add_argument('name', help='the name of the problem')
parser.add_argument('number', nargs='?', default="", help='id of the sample')
parser.add_argument('-a', '--asan', action="store_true", help='enable asan (fsanitize=address,undefined) [currently not available when compiling on windows]')
parser.add_argument('-k', '--kattis', action="store_true", help='submit to kattis')
parser.add_argument('-K', '--KATTIS', action="store_true", help='submit to kattis (skip submission check)')
args = parser.parse_args()
args.name = args.name.strip('/')

source = glob.glob(args.name + "/src/*.cpp")

print("compiling...")
options = ["-O2", "-std=c++11", "-g", "-ggdb", "-Wall", "-Wextra", "-pedantic" ]
if args.asan: options += [ "-fsanitize=address,undefined" ]
else: options += [ "-static" ] # used by kattis, but incompatible with asan
subprocess.check_call([shutil.which("g++")] + options + ["-I_library", "-o", args.name + "/" + args.name + ".exe"]  + source)
dependencystr = subprocess.check_output([shutil.which("g++"), "-std=c++11", "-MM", "-I_library"] + source).decode()
dependencies = set()
for d in re.finditer(r"^[^:]+:((?:[^\r\n\\]|\\\r?\n?)*(?:\\\r?$(?:[^\r\n\\]|\\\r?\n?)*)*)\r?$", dependencystr, re.MULTILINE):
	for dep in re.finditer(r"(?:[^\s\\]|\\(?!\r?$))+", d.group(1), re.MULTILINE):
		dependencies.add(dep.group(0))
print("compilation successful")

print("testing program...")
if args.number == "":
	tests = (os.path.basename(x)[:-3] for x in glob.iglob(args.name + "/samples/*.in"))
else: tests = [args.name + "-" + args.number]
for test in tests:
	print("Test ", test, ":", sep='')
	with open(args.name + "/samples/" + test + ".in") as f:
		call = subprocess.check_output([args.name + "/" + args.name + ".exe"], stdin=f).decode()
	print(call)
	with open(args.name + "/samples/" + test + ".ans", "rt") as f:
		testlines = call.splitlines()
		anslines = [line.strip('\n') for line in f]
		skipverification = False
		if(len(anslines) != len(testlines)):
			print("ERROR: OUTPUT IS NOT CORRECT (incorrect number of lines: was ", len(testlines), " but expected ", len(anslines), ")", sep="")
			result = input("Continue anyway? [y/N] ")
			if result == 'n' or result == 'N' or result == '':
				sys.exit(1)
			elif result == 'y' or result == 'Y':
				skipverification = True
		for t in zip(range(len(testlines)), anslines, testlines):
			if skipverification: break
			if t[1].strip('\n') != t[2]:
				print("ERROR: OUTPUT IS NOT CORRECT (difference in line ", t[0] + 1, ")", sep='')
				while not skipverification:
					result = input("Continue anyway? [y/N] ")
					if result == 'n' or result == 'N' or result == '':
						sys.exit(1)
					elif result == 'y' or result == 'Y':
						skipverification = True
	print()
print("program test successful")
		
if args.kattis or args.KATTIS:
	print("submitting to kattis...")
	call = [sys.executable, "submit.py", "-p", args.name, "-l", "C++"]
	if args.KATTIS: call.append('-f')
	subprocess.check_call(call + source + list(dependencies))