# -*- coding: utf-8 -*-
"""
Created on Sun May 10 19:19:01 2015

@author: andric
"""

import os
import time
import pandas as pd
import numpy as np
import random
import graph_evals as ge

if __name__ == '__main__':

    os.chdir(os.environ['pnd'])
    print os.getcwd()

    df = pd.read_csv('pandit_data.csv')
    p_df = df.iloc[0:21, 1:]
    c_df = df.iloc[21:42, 1:]
    subj_list = ['pandit', 'ctrl']
    dat = []
    dat.append(p_df)
    dat.append(c_df)
    pc_dat = dict(zip(subj_list, dat))

    #for d in pc_dat:
    for d in ['pandit']:
        for thresh_dens in np.arange(.1, .51, .1):
            print 'Thresh: %s' % thresh_dens
            print time.ctime()
            subjid = d
            dat_dir = os.environ['pnd']+'/AB_tests/'
            if not os.path.exists(dat_dir):
                os.makedirs(dat_dir)
            graph_loc = 'graphs'
            graph_dir = os.path.join(dat_dir, graph_loc)
            if not os.path.exists(graph_dir):
                os.makedirs(graph_dir)

            niter = 100
            avg_r_a = np.zeros(niter)
            avg_r_b = np.zeros(niter)
            for x in xrange(niter):
                samp = random.sample(range(21), 20)
                a = random.sample(samp, 10)
                b = list(set(samp) - set(a))
                samp_dict = dict(zip(['a', 'b'], [a, b]))
                for samp in samp_dict:
                    df = pc_dat[d].iloc[samp_dict[samp], 1:]
                    graph_outname = 'iter%d.%s.%s.dens_%s.edgelist.gz' % \
                                    (x, samp, subjid, thresh_dens)

                    gr = ge.GRAPHS(subjid, df,
                                   thresh_dens, graph_dir,
                                   os.path.join(graph_dir, graph_outname))

                    # making graph:
                    if samp is 'a':
                        avg_r_a[x] = gr.make_graph()
                    elif samp is 'b':
                        avg_r_b[x] = gr.make_graph()

                    # get modularity and trees
                    print 'Doing modularity evaluation... '
                    print time.ctime()
                    n_nodes = 148
                    g = gr.make_networkx_graph(n_nodes)

                    mod_loc = 'modularity'
                    mod_dir = os.path.join(dat_dir, mod_loc)
                    if not os.path.exists(mod_dir):
                        os.makedirs(mod_dir)

                    Qs = np.zeros(niter)
                    trees = np.zeros(n_nodes*niter).reshape(n_nodes, niter)
                    for i in xrange(niter):
                        trees[:, i], Qs[i] = gr.get_modularity(g)
                    Qs_outname = 'iter%d.%s.%s.dens_%s.Qval' % \
                        (x, samp, subjid, thresh_dens)
                    np.savetxt(os.path.join(mod_dir, Qs_outname),
                               Qs, fmt='%.4f')
                    trees_outname = 'iter%d.%s.%s.dens_%s.trees' % \
                        (x, samp, subjid, thresh_dens)
                    np.savetxt(os.path.join(mod_dir, trees_outname),
                               trees, fmt='%i')

            avg_r_val_a_name = 'Avg_r_val_a_%s.dens_%s.txt' % \
                (subjid, thresh_dens)
            avg_r_val_b_name = 'Avg_r_val_b_%s.dens_%s.txt' % \
                (subjid, thresh_dens)
            avg_r_a_out = os.path.join(graph_dir, avg_r_val_a_name)
            avg_r_b_out = os.path.join(graph_dir, avg_r_val_b_name)
            np.savetxt(avg_r_a_out, avg_r_b, fmt='%.4f')
            np.savetxt(avg_r_b_out, avg_r_b, fmt='%.4f')
