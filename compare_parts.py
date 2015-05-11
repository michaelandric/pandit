# -*- coding: utf-8 -*-
"""
Created on Sun May 10 23:20:29 2015

@author: andric
"""

import os
import graph_evals as ge
import numpy as np
from itertools import combinations


dat_dir = os.environ['pnd']+'/AB_tests'
os.chdir(dat_dir)
print os.getcwd()
niter = 100
n_regions = 148
modularity_loc = 'modularity'
modularity_dir = os.path.join(dat_dir, modularity_loc)
out_dir = dat_dir+'/similarity_measures/'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for thresh_density in ['0.1', '0.2', '0.3', '0.4', '0.5']:
    subjid1 = 'pandit'
    subjid2 = 'ctrl'
    # subjid2 = subjid1
    # subjid1 = subjid2
    n_combinations = ((niter**2)-niter)/2
    compare_out = np.array(np.zeros(n_combinations))   # prep output array

    # Building array of inputs. These are the trees of highest modularity
    tree_mat1 = np.array(np.zeros(niter*n_regions))
    tree_mat1 = tree_mat1.reshape(n_regions, niter)
    tree_mat2 = np.array(np.zeros(niter*n_regions))
    tree_mat2 = tree_mat2.reshape(n_regions, niter)

    for n in xrange(niter):
        print n
        a_Q_pref = 'iter%d.a.%s.dens_%s.Qval' % \
            (n, subjid1, thresh_density)
        a_Qs = np.loadtxt(os.path.join(modularity_dir, a_Q_pref))
        tree1_name = 'iter%d.a.%s.dens_%s.trees' % \
            (n, subjid1, thresh_density)
        trees_a = np.loadtxt(os.path.join(modularity_dir, tree1_name))
        a_max = a_Qs.argmax()
        tree_mat1[:, n] = trees_a[:, a_max]

        b_Q_pref = 'iter%d.b.%s.dens_%s.Qval' % \
            (n, subjid2, thresh_density)
        b_Qs = np.loadtxt(os.path.join(modularity_dir, b_Q_pref))
        tree2_name = 'iter%d.b.%s.dens_%s.trees' % \
            (n, subjid2, thresh_density)

        trees_b = np.loadtxt(os.path.join(modularity_dir, tree2_name))
        b_max = b_Qs.argmax()
        tree_mat2[:, n] = trees_b[:, b_max]

    # Main section to run. DOING BOTH ARI AND NMI
    output_pref = 'between%s_%s_dens_%s_ARI.txt' % \
        (subjid1, subjid2, thresh_density)
    # output_pref = 'within%s_dens%s_ARI.txt' % (subjid1, thresh_density)
    # output_pref = 'within%s_dens%s_ARI.txt' % (subjid2, thresh_density)
    for i, combo in enumerate(combinations(np.arange(100), 2)):
        tree_a = tree_mat1[:, combo[0]]
        tree_b = tree_mat2[:, combo[1]]
        compare_out[i] = ge.adj_rand(tree_a, tree_b)
    np.savetxt(os.path.join(out_dir, output_pref), compare_out, fmt='%.4f')

    output_pref = 'between%s_%s_dens_%s_NMI.txt' % \
        (subjid1, subjid2, thresh_density)
    # output_pref = 'within%s_dens%s_NMI.txt' % (subjid1, thresh_density)
    # output_pref = 'within%s_dens%s_NMI.txt' % (subjid2, thresh_density)
    for i, combo in enumerate(combinations(np.arange(100), 2)):
        tree_a = tree_mat1[:, combo[0]]
        tree_b = tree_mat2[:, combo[1]]
        compare_out[i] = ge.normalized_MI(tree_a, tree_b)
    np.savetxt(os.path.join(out_dir, output_pref), compare_out, fmt='%.4f')
