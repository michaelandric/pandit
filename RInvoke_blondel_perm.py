#!/usr/bin/python

import os
import sys
from subprocess import call
from subprocess import Popen
import shutil

"""
This takes batch starts and finishes. 
"""
R_SCRIPT_PREFIX = sys.argv[1]
#group = sys.argv[2]   # this is either 'A' or 'B' for a permutation
start = sys.argv[2]   # the permutation number
finish = sys.argv[3]

for i in range(int(start), int(finish) + 1):
    for group in ["A", "B"]:
        os.environ["R_ARGS"] = group+" "+`i`
        WORKDIR = "/mnt/tier2/urihas/Andric/pandit/perm/"
        R_SCRIPT = R_SCRIPT_PREFIX+".R"
        R_SCRIPT_NEW = WORKDIR+R_SCRIPT_PREFIX+"_"+group+"_"+`i`+".R"
        shutil.copy2(R_SCRIPT, R_SCRIPT_NEW)
        os.chdir(WORKDIR)

        print os.getcwd()
        proc = Popen("R CMD BATCH --vanilla "+R_SCRIPT_NEW, shell = True)
        proc.wait()
        
        fname = R_SCRIPT_NEW+"out"
        f = open(fname, "r")
        searchlines = f.readlines()
        levelset = []
        for line in searchlines:
            if "level" in line:
                levelset.append(line)

        hier = len(levelset) - 1
        os.environ["R_ARGS"] = group+" "+`i`+" "+`hier`
        R_SCRIPT_HIERARCHY = "/mnt/tier2/urihas/Andric/pandit/code/9.exec_blondel_hier.R"
        call("R CMD BATCH --vanilla "+R_SCRIPT_HIERARCHY, shell = True)
        os.chdir("/mnt/tier2/urihas/Andric/pandit/code/")

