# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:09:13 2015

@author: andric

This is a prior to mapnames.py.
Can just give the hexs and rgb vals as
a list.
Get those easily here:
http://tools.medialab.sciences-po.fr/iwanthue/

"""

import os
import pandas as pd
import numpy as np

hexs = ["#C557DF",
        "#5BD83C",
        "#D6421F",
        "#7DCFE0",
        "#34341A",
        "#D08698",
        "#E2AC31",
        "#69A874",
        "#363056",
        "#608FD9",
        "#9F3988",
        "#7C361C",
        "#DD4466",
        "#D2B373",
        "#4B1A27",
        "#928674",
        "#D5C5CB",
        "#63509C",
        "#D78266",
        "#A0A83A",
        "#5E7391",
        "#D588CE",
        "#66DF7B",
        "#D97B2F",
        "#5C6625",
        "#B4E13E",
        "#4D9133",
        "#BAE185",
        "#72E4BB",
        "#CCD7B1",
        "#2D4249",
        "#976E2F",
        "#3B6748",
        "#B4A5D4",
        "#983A4F",
        "#7F70DD",
        "#5EA29D",
        "#DB43B9",
        "#E3DA48",
        "#704D49",
        "#DE4B8C",
        "#713969",
        "#CF4240"]

rgbs = [[197,87,223],
        [91,216,60],
        [214,66,31],
        [125,207,224],
        [52,52,26],
        [208,134,152],
        [226,172,49],
        [105,168,116],
        [54,48,86],
        [96,143,217],
        [159,57,136],
        [124,54,28],
        [221,68,102],
        [210,179,115],
        [75,26,39],
        [146,134,116],
        [213,197,203],
        [99,80,156],
        [215,130,102],
        [160,168,58],
        [94,115,145],
        [213,136,206],
        [102,223,123],
        [217,123,47],
        [92,102,37],
        [180,225,62],
        [77,145,51],
        [186,225,133],
        [114,228,187],
        [204,215,177],
        [45,66,73],
        [151,110,47],
        [59,103,72],
        [180,165,212],
        [152,58,79],
        [127,112,221],
        [94,162,157],
        [219,67,185],
        [227,218,72],
        [112,77,73],
        [222,75,140],
        [113,57,105],
        [207,66,64]]

column_names = ['group', 'module', 'colorHEX', 'colorRGB']

dens = '0.1'
module_ids = []
g_names = []

basedir = '/Users/andric/Documents/workspace/pandit'
for g in ['pandit', 'ctrl']:
    g_file = '%s.inclusionlist.dens_%s.csv' % (g, dens)
    g_inclu = pd.read_csv(os.path.join(basedir, g_file))
    mods = np.array(np.unique(g_inclu.loc[:, 'community']), dtype=int)
    module_ids.append(mods)
    g_names.append([g]*len(mods))

modules = np.concatenate(module_ids)
g_names = np.concatenate(g_names)

mods_names_colors = zip(g_names, modules, hexs, rgbs)
out_frame = pd.DataFrame(mods_names_colors, columns=column_names)
out_name = 'colors_pandit_ctrl.dens_%s.csv' % dens
out_frame.to_csv(os.path.join(basedir, out_name), index=False)
