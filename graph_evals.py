# -*- coding: utf-8 -*-
"""
Created on Sun May 10 12:35:08 2015

@author: andric
"""

import os
import time
import numpy as np
import networkx as nx
import bct


class GRAPHS:

    def __init__(self, subjid, inputTS, thresh_density,
                 graph_dir, edgelist_name):
        """
        Initialize for hel
        :param subjid: subject identifier
        :param inputTS: the time series for input
        :param thresh_density: This is the threshold
        :return:
        """
        self.ss = subjid
        self.dens = float(thresh_density)
        self.input = inputTS
        self.graph_dir = graph_dir
        self.el_name = edgelist_name
        print 'Initializing. -- '+time.ctime()

    def make_graph(self):
        """
        Makes graph by pairwise correlation
        Threshold at density
        Returns average correlation among values
        """
        print 'Now making graph -- '+time.ctime()
        ts = self.input.T   # this need to transpose
        n_vox = ts.shape[0]
        compl_graph = int((n_vox*(n_vox-1))/2)
        n_edges = int(compl_graph*self.dens)
        print 'Input is read. '
        print 'Now getting the correlation matrix. '+time.ctime()
        corrmat = np.corrcoef(ts)
        corrmat_ut = np.nan_to_num(np.triu(corrmat, k=1))
        print 'Starting sort. -- '+time.ctime()
        corrsrtd = np.sort(corrmat_ut[corrmat_ut > 0], kind='mergesort')
        print 'Sort done. \nThresholding... -- '+time.ctime()
        threshd = corrsrtd[-n_edges:]
        print 'Thresholding done. \nNow getting edge indices -- '+time.ctime()
        ix = np.searchsorted(threshd, corrmat_ut, 'right')
        n, v = np.where(ix)
        inds = np.array(zip(n, v), dtype=np.int32)
        print 'Got graph edges. \nWriting it to file -- '+time.ctime()
        np.savetxt(self.el_name, inds, fmt='%d')
        print 'Graph edgelist written out. \nDONE. -- '+time.ctime()
        return np.mean(threshd)

    def make_networkx_graph(self, n_nodes):
        # setting it up for further use
        g = nx.Graph()
        g.add_nodes_from(range(148))
        ed = nx.read_edgelist(os.path.join(self.graph_dir, self.el_name),
                              nodetype=int)
        g.add_edges_from(ed.edges())
        return g

    def get_modularity(self, graph):
        """
        Gets modularity louvain
        Uses bct package
        Returns communities and modularity value
        at highest level
        :param graph: Input graph via networkx
        :return c: communities
        :return q: modularity value
        """
        c, q = bct.modularity_louvain_und(nx.adjacency_matrix(graph).toarray())
        return (c, q)
