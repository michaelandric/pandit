# -*- coding: utf-8 -*-
"""
Created on Thu May 14 16:21:44 2015

@author: andric
"""

import os
import networkx as nx
import bct
import numpy as np


def make_networkx_graph(n_nodes, edgelist_name):
    g = nx.Graph()
    g.add_nodes_from(range(n_nodes))
    ed = nx.read_edgelist(edgelist_name, nodetype=int)
    g.add_edges_from(ed.edges())
    return g


if __name__ == '__main__':

    dat_dir = os.environ['pnd']
    graph_dir = dat_dir+'/graphs/'
    modularity_dir = dat_dir+'/modularity/'
    role_dir = dat_dir+'/node_roles'
    if not os.path.exists(role_dir):
        os.makedirs(role_dir)
    nnodes = 148

    for subjid in ['pandit', 'ctrl']:
        thresh_dens = '0.1'
        qscores = '%s.dens_%s.Qval' % (subjid, thresh_dens)
        df = np.loadtxt(os.path.join(modularity_dir, qscores))
        maxiter = df.argmax()
        trees_name = '%s.dens_%s.trees' % (subjid, thresh_dens)
        trees_in = os.path.join(modularity_dir, trees_name)
        coms = np.loadtxt(trees_in)[:, maxiter]

        graph_name = '%s.dens_%s.edgelist.gz' % (subjid, thresh_dens)
        g = make_networkx_graph(nnodes, os.path.join(graph_dir, graph_name))
        ga = nx.adjacency_matrix(g).toarray()

        pc = bct.participation_coef(ga, coms)
        wz = bct.module_degree_zscore(ga, coms)

        pc_out_name = '%s.dens_%s_part_coef.txt' % (subjid, thresh_dens)
        np.savetxt(os.path.join(role_dir, pc_out_name), pc, fmt='%.4f')
        wz_out_name = '%s.dens_%s_within_mod_Z.txt' % (subjid, thresh_dens)
        np.savetxt(os.path.join(role_dir, wz_out_name), wz, fmt='%.4f')
