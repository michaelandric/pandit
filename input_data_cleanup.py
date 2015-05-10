# -*- coding: utf-8 -*-
"""
Created on Sun May 10 10:56:50 2015

re-arrange data setup

@author: andric
"""

import pandas as pd

lh = pd.read_table('2015.lh.aparcstats.andric.txt')
rh = pd.read_table('2015.rh.aparcstats.andric.txt')
pieces = [lh.iloc[:, 1:75], rh.iloc[:, 1:75]]
new_dat = pd.concat(pieces, axis=1)
pnd = []
ctrl = []
for i in range(21):
    pnd.append('pandit_%d' % i)
    ctrl.append('ctrl_%d' % i)

newind = pd.DataFrame(pnd+ctrl, columns=['subj'])
newpieces = [newind, new_dat]
dat2 = pd.concat(newpieces, axis=1)
dat2.to_csv('pandit_data.csv', index=False)
