#!/usr/bin/python

import os
import sys
from subprocess import call


os.environ["R_ARGS"] = ' '.join(sys.argv[2:])

call("R CMD BATCH --vanilla "+sys.argv[1], shell = True)
