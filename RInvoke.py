#!/usr/bin/python

import os
import sys
from subprocess import call


os.environ["R_ARGS"] = ' '.join(sys.argv[1:])

call("R CMD BATCH --vanilla "+sys.argv[0], shell = True)
