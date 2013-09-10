#!/usr/bin/python

import os
import sys
from subprocess import call
import shutil

R_SCRIPT_PREFIX = sys.argv[1]
group = sys.argv[2]
hemi = sys.argv[3]
thresh = sys.argv[4]

os.environ["R_ARGS"] = ' '.join(sys.argv[2:])
WORKDIR = "/mnt/tier2/urihas/Andric/pandit/"
R_SCRIPT = R_SCRIPT_PREFIX+".R"
R_SCRIPT_NEW = R_SCRIPT_PREFIX+"_"+group+"_"+hemi+"_"+thresh+".R"
shutil.copy2(R_SCRIPT, WORKDIR+R_SCRIPT_NEW)
os.chdir(WORKDIR)

print os.getcwd()
call("R CMD BATCH --vanilla "+R_SCRIPT_NEW, shell = True)

