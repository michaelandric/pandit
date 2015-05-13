# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:46:38 2015

@author: andric
"""

import os
import numpy as np
import pandas as pd
import networkx as nx

if __name__ == '__main__':

    dat_dir = os.environ['pnd']
    modularity_dir = dat_dir+'/modularity'
    graph_dir = dat_dir+'/graphs'
    dat_file = 'pandit_data.csv'
    df = pd.read_csv(os.path.join(dat_dir, dat_file))
    ctnames = pd.Series(df.columns[1:])
    subj_list = ['pandit', 'ctrl']
    cols = ['nodes', 'coms']
    dfcols = ['region', 'community']

    for subjid in subj_list:
        for thresh_dens in np.arange(.2, .51, .1):
            q_name = '%s.dens_%s.Qval' % (subjid, thresh_dens)
            qscores = np.loadtxt(os.path.join(modularity_dir, q_name))
            maxiter = qscores.argmax()
            t_name = '%s.dens_%s.trees' % (subjid, thresh_dens)
            trees = np.loadtxt(os.path.join(modularity_dir, t_name))
            g_name = '%s.dens_%s.edgelist.gz' % (subjid, thresh_dens)
            g = nx.read_edgelist(os.path.join(graph_dir, g_name), nodetype=int)

            tmp_mx = np.column_stack((np.arange(148), trees[:, maxiter]))
            max_tree = pd.DataFrame(tmp_mx, columns=cols)
            max_tree = max_tree.iloc[g.nodes(), :]

            # max_tree = trees[:, maxiter]
            nnames = []
            modid = []
            for com in set(max_tree.loc[:, 'coms']):
                ns = max_tree.loc[:, 'nodes'][max_tree.loc[:, 'coms'] == com]
                list_nodes = map(int, ns)
                nnames.append(ctnames[list_nodes])
                modid.append(np.repeat(com, len(list_nodes)))
            nnames = list(np.concatenate(nnames))
            modid = list(np.concatenate(modid))
            newd = pd.DataFrame(zip(nnames, modid), columns=dfcols)
            mod_list_name = '%s.inclusionlist.dens_%s.csv' % \
                (subjid, thresh_dens)
            newd.to_csv(os.path.join(dat_dir, mod_list_name))
