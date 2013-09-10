#!/usr/bin/python

"""
Here's how you use this on the command line:
python exec_makesubmitargs.py >> submit.try
where 'submit.try' is the condor_submit file that you're adding arguments to
"""

from makeargs import makearg as mm

groups = ["ctrl", "pandit"]
hemispheres = ["lh", "rh"]

for g in groups:
    for h in hemispheres:
        #mm.fcorr_args(g, h)
        mm.threshold_convert_args(g, h)