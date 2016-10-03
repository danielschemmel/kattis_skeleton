# Kattis Skeleton

This repository provides a skeleton to write C++ programs for [Kattis](https://open.kattis.com).
It will automatically download sample input and solution files, create and manage a folder structure, verify your solution and turn it in.

## Usage

```bash
python setup.py $PROBLEMID
# do some work
python run.py $PROBLEMID
# fix some bugs
python run.py -K $PROBLEMID
# profit!
```

## Prerequisites

The Kattis submission client requires a `.kattisrc` file, which can be downloaded from [here (requires login to Kattis)](https://open.kattis.com/download/kattisrc).
Simply save it in your home folder (check that the file is really saved under the name `.kattisrc`) and you are good to go.

You will need some sort of Python installation.
This projects assumes a new Python 3, and may or may not work with older versions (e.g. Python 2).

To compile the solutions for local verification, [g++](https://gcc.gnu.org/) is required.
For maximum compatibility with Kattis, check the [Kattis C++ FAQ](https://open.kattis.com/help/cpp) on which version to use.

Additionally, a version of [curl](https://curl.haxx.se/) is required to download the sample files.

### Linux
Just ask your package manager to get everything you need.
E.g. for Arch your might want to do something like:

```bash
sudo pacman -S --needed python python-requests base-devel curl
```

### Windows
Download and install [Anaconda](https://www.continuum.io/downloads) for Python 3.
It includes Python 3, all required packages and additionally a version of `curl`.

Download and install [msys2](http://msys2.github.io/).
Open the msys2 shell (or let it open automatically at the end of the installation) and run `pacman -S --needed mingw-w64-x86_64-toolchain`.
Add `C:\msys64\mingw64\bin` (or equivalent) to your path.