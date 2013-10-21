#!/usr/bin/python

"""
Here's how you use this on the command line:
python exec_makesubmitargs.py >> submit.try
where 'submit.try' is the condor_submit file that you're adding arguments to
"""

from makeargs import makearg as mm

groups = ["ctrl", "pandit"]
hemispheres = ["lh", "rh"]

#for g in groups:
#    mm.hierarchy_args(g)
    #for h in hemispheres:
        #mm.fcorr_args(g, h)
        #mm.threshold_convert_args(g, h)
        #mm.blondel_args(g, h)


total = 1000
batch_size = 100
batch_starts = range(1, total, batch_size)
ends = []
for i in batch_starts:
    ends.append(i + (batch_size - 1))

ends[len(ends) - 1] = total 

for i in range(0, len(batch_starts)):
    #mm.batch_perms2(batch_starts[i], ends[i])
    #mm.batch_blondel_hier_perms(batch_starts[i], ends[i])
    mm.batch_nmi_perms(batch_starts[i], ends[i])
