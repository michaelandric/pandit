#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 2015

@author: andric
"""

import os
import time
import pandas as pd
import numpy as np
import graph_evals as ge

if __name__ == '__main__':

    dat_dir = os.environ['pnd']
    random_dir = dat_dir+'/random/'
    if not os.path.exists(random_dir):
        os.makedirs(random_dir)
    random_graph_dir = random_dir+'/graphs/'
    if not os.path.exists(random_graph_dir):
        os.makedirs(random_graph_dir)
    df = pd.read_csv(os.path.join(dat_dir, 'pandit_data.csv'))
    p_df = df.iloc[0:21, 1:]
    c_df = df.iloc[21:42, 1:]
    subj_list = ['pandit', 'ctrl']
    dat = []
    dat.append(p_df)
    dat.append(c_df)
    pc_dat = dict(zip(subj_list, dat))
    n_nodes = 148
    niter = 100
    mod_loc = 'modularity'
    mod_dir = os.path.join(random_dir, mod_loc)
    if not os.path.exists(mod_dir):
        os.makedirs(mod_dir)

    for d in pc_dat:
        for thresh_dens in np.arange(.1, .51, .1):
            print 'Thresh: %s' % thresh_dens
            print time.ctime()
            subjid = d
            graph_dir = os.path.join(dat_dir, 'graphs')
            if not os.path.exists(graph_dir):
                os.makedirs(graph_dir)
            graph_outname = '%s.dens_%s.edgelist.gz' % (subjid, thresh_dens)

            gr = ge.GRAPHS(subjid, pc_dat[d],
                           thresh_dens, graph_dir,
                           os.path.join(graph_dir, graph_outname))

            Qs = np.zeros(niter)
            for n in xrange(niter):
                rand_name = 'iter%d_rand_%s.dens_%s.Qval' % \
                    (n, subjid, thresh_dens)
                rand_file = os.path.join(mod_dir, rand_name)
                Qs[n], iterq = gr.max_q(rand_file)
            Qs_outname = 'rand_%s.dens_%s.Qval' % (subjid, thresh_dens)
            np.savetxt(os.path.join(mod_dir, Qs_outname), Qs, fmt='%.4f')
