# -*- coding: utf-8 -*-
"""
Created on Sun May 10 16:47:15 2015

@author: andric
"""

import os
import time
import pandas as pd
import numpy as np
import graph_evals as ge
import networkx as nx


if __name__ == '__main__':

    os.chdir(os.environ['pnd'])
    print os.getcwd()

    dat_dir = os.environ['pnd']
    random_dir = dat_dir+'/random/'
    if not os.path.exists(random_dir):
        os.makedirs(random_dir)
    random_graph_dir = random_dir+'/graphs/'
    if not os.path.exists(random_graph_dir):
        os.makedirs(random_graph_dir)
    df = pd.read_csv('pandit_data.csv')
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

            g = gr.make_networkx_graph(n_nodes)
            for n in xrange(niter):
                deg = int(np.mean(g.degree().values()))
                g_rand = nx.random_regular_graph(deg, n_nodes)
                outg_pref = 'iter%d_rand_%s.dens_%s.edgelist.gz' % \
                    (n, subjid, thresh_dens)
                outg = os.path.join(random_graph_dir, outg_pref)
                nx.write_edgelist(g_rand, outg, data=False)

                # get modularity and trees
                print 'Doing modularity evaluation... '
                print time.ctime()
                Qs = np.zeros(niter)
                trees = np.zeros(n_nodes*niter).reshape(n_nodes, niter)
                for i in xrange(niter):
                    trees[:, i], Qs[i] = gr.get_modularity(g_rand)
                Qs_outname = 'iter%d_rand_%s.dens_%s.Qval' % \
                    (n, subjid, thresh_dens)
                np.savetxt(os.path.join(mod_dir, Qs_outname), Qs, fmt='%.4f')
                trees_outname = 'iter%d_rand_%s.dens_%s.trees' % \
                    (n, subjid, thresh_dens)
                np.savetxt(os.path.join(mod_dir, trees_outname),
                           trees, fmt='%i')
