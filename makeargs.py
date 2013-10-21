#!/usr/bin/python

import os
from optparse import OptionParser

class MakeArgs:

    def get_opts(self):
        desc = """Generate args for condor submit scripts"""
        self.usage = "usage: %prog [options]"
        self.parser = OptionParser(description = desc, version = "%prog September 2013")
        self.parser.add_option("--subject", desc = "subject",
                                help = "specify the subject")
        self.parser.add_option("--arg1", desc = "arg1",
                                help = "give the first argument")
                                
        (self.options, args) = self.parser.parse_args()
        
    def fcorr_args(self, group, arg1):
        """
        'group' is either ctrl or pandit
        'arg1' is hemisphere
        """
        print "arguments    = 1.corr_matrix.R "+group+" "+arg1+" \nqueue \n"
        
    def threshold_convert_args(self, group, arg1):
        print "arguments    = 2.threshold_convert.R "+group+" "+arg1+" \nqueue \n"

    def blondel_args(self, group, arg1):
        """
        'arg1' is hemisphere
        'arg2' is threshold
        """
        print "arguments   = 3.blondel "+group+" "+arg1+" 0.5 \nqueue \n"

    def hierarchy_args(self, group):
        print "arguments   = 4.hierarchy.R "+group+" \nqueue \n"

    def batch_perms(self, arg1, arg2):
        print "arguments    = 6.perm_run.R "+`arg1`+" "+`arg2`+" \nqueue \n"

    def batch_perms2(self, arg1, arg2):
        print "arguments    = 7.perm_thresh_convert.R "+`arg1`+" "+`arg2`+" \nqueue \n"

    def batch_blondel_hier_perms(self, arg1, arg2):
        print "arguments    = 8.blondel_perm "+`arg1`+" "+`arg2`+" \nqueue \n"



makearg = MakeArgs()
