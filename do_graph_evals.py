# -*- coding: utf-8 -*-
"""
Created on Sun May 10 16:47:15 2015

@author: andric
"""

import os
import pandas as pd
import numpy as np
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

    for d in pc_dat:
        thresh_dens = .1
        subjid = d
        dat_dir = os.environ['pnd']
        graph_loc = 'graphs'
        graph_dir = os.path.join(dat_dir, graph_loc)
        if not os.path.exists(graph_dir):
            os.makedirs(graph_dir)
        graph_outname = '%s.dens_%s.edgelist.gz' % (subjid, thresh_dens)

        gr = ge.GRAPHS(subjid, pc_dat[d],
                       thresh_dens, graph_dir,
                       os.path.join(graph_dir, graph_outname))

        # making graph:
        avg_r = gr.make_graph()
        avg_r_val_name = 'Avg_r_val_%s.dens_%s.txt' % (subjid, thresh_dens)
        avg_r_out = os.path.join(graph_dir, avg_r_val_name)
        np.savetxt(avg_r_out, avg_r, fmt='%.4f')

        # get modularity and trees
        n_nodes = 148
        g = gr.make_networkx_graph(n_nodes)

        mod_loc = 'modularity'
        mod_dir = os.path.join(dat_dir, mod_loc)
        if not os.path.exists(mod_dir):
            os.makedirs(mod_dir)
        niter = 100
        Qs = np.zeros(niter)
        trees = np.zeros(n_nodes*niter).reshape(n_nodes, niter)
        for i in xrange(niter):
            c, q = gr.get_modularity(g)
            Qs[i] = q
            trees[:, i] = c
        Qs_outname = '%s.dens_%s.Qval' % (subjid, thresh_dens)
        np.savetxt(os.path.join(mod_dir, Qs_outname), Qs, fmt='%.4f')
        trees_outname = '%s.dens_%s.trees' % (subjid, thresh_dens)
        np.savetxt(os.path.join(mod_dir, trees_outname),
                   trees, fmt='%i')
