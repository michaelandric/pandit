# -*- coding: utf-8 -*-
"""
Created on Mon May 18 16:51:34 2015

@author: andric

How I got the surface node labels from the anot file:

ConvertDset -i lh.aparc.a2009s.annot.niml.dset -o_1Dp \
-prepend_node_index_1D -prefix lh_node_labels
ConvertDset -i rh.aparc.a2009s.annot.niml.dset -o_1Dp \
-prepend_node_index_1D -prefix rh_node_labels
"""

import time
import os
import pandas as pd
import numpy as np
from ast import literal_eval

suma_dir = '/Applications/AFNI/suma_MNI_N27/'
basedir = '/Users/andric/Documents/workspace/pandit/'
ct = pd.read_csv(os.path.join(basedir, 'pandit_data.csv'))
ctnames = pd.Series(ct.columns[1:], name='region_name')

# see above for how I made these 1D labels files
lh_labels = np.loadtxt(os.path.join(basedir, 'lh_node_labels.1D.dset'))
rh_labels = np.loadtxt(os.path.join(basedir, 'rh_node_labels.1D.dset'))

# this is same as "lh.aparc.a2009s.annot.1D.cmap" and
# "rh.aparc.a2009s.annot.1D.cmap"
cmap_f = 'rois.aparc.cmap'
rois = open(os.path.join(basedir, cmap_f), 'r').readlines()

# for dens in ['0.2', '0.3', '0.4', '0.5', '0.6']:
for dens in ['0.1']:
    clrs_fname = 'colors_pandit_ctrl.dens_%s.csv' % dens
    clrs = pd.read_csv(os.path.join(basedir, clrs_fname))
    clrs_frc = []
    new_crgb = clrs['colorRGB'].apply(literal_eval)
    for i in xrange(len(new_crgb)):
        clrs_frc.append([round(num/255., 5) for num in new_crgb[i]])
    nm_rows = np.array(rois)[np.arange(1719, 1869, 2)]
    idents = np.array(map(int,
                          [rw.split()[5].split('(')[1].split(')')[0]
                              for rw in nm_rows]))
    idents_f = np.delete(idents, np.where(np.in1d(idents, 1644825)))

    lh_idents_dict = dict(zip(np.array(idents_f), ctnames[0:74]))
    rh_idents_dict = dict(zip(np.array(idents_f), ctnames[74:148]))

    for g in ['pandit', 'ctrl']:
        inclu_fname = '%s.inclusionlist.dens_%s.csv' % (g, dens)
        g_inclu = pd.read_csv(os.path.join(basedir, inclu_fname))
        g_dict = dict(zip(g_inclu.iloc[:, 1], g_inclu.iloc[:, 2]))
        for h in ['lh', 'rh']:
            print '%s -- %s -- ' % (g, h)+time.ctime()
            roi_aparc = '%s.aparc.a2009s.annot.1D.roi' % h
            aparc = np.loadtxt(os.path.join(suma_dir, roi_aparc))
            new_rgb = np.array(np.zeros(len(aparc)*3)).reshape(len(aparc), 3)
            if h == 'lh':
                lbls = lh_labels
                indents_dict = lh_idents_dict
            elif h == 'rh':
                lbls = rh_labels
                indents_dict = rh_idents_dict

            for i in xrange(len(lbls[:, 1])):
                try:
                    m = int(g_dict[indents_dict[int(lbls[:, 1][i])]])
                    tt = clrs[clrs['group'] == g]
                    new_rgb[i, :] = clrs_frc[tt[tt['module'] == m].index[0]]
                except:
                    new_rgb[i, :] = np.zeros(3)
            new_rgb_out_f = np.column_stack((aparc[:, 0], new_rgb))
            mod_rgb_out_fname = '%s_%smod_labels.dens_%s.1D' % (h, g, dens)
            np.savetxt(os.path.join(basedir, mod_rgb_out_fname),
                       new_rgb_out_f, fmt='%i %f %f %f')
