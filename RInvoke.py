#!/usr/bin/python

import os
import sys
from subprocess import call

print sys.argv
os.environ["R_ARGS"] = sys.argv[1:]

call("R CMD BATCH --vanilla "+sys.argv[0], shell = True)
