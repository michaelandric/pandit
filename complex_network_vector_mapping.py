# -*- coding: utf-8 -*-
"""
Created on Thu May 21 13:55:19 2015

@author: andric

orig in Sandro's code
https://github.com/svegapons/graph_kernels/blob/master/uri_data_test.py

"""

import os
import numpy as np
import networkx as nx
from bct import *
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score, KFold


def complex_network_mapping(graph):
    """
    Compute the vectorial mapping of a graph based on the computation of
    several complex-network analysis indexes.
    """
    vect = []

    n = nx.number_of_nodes(graph)
    e = nx.number_of_edges(graph)
    print n, e

#    adj = nx.adjacency_matrix(graph).toarray()
#    adj_bin = np.where(adj > 0, 1., 0.)
#    adj_conn = 1 - adj
    adj_bin = nx.adjacency_matrix(graph).toarray()
    adj_bin = np.array(adj_bin, dtype=np.float)

    # Node Betweenness binary
    bt_bin = nx.betweenness_centrality(graph).values()
    avg_btb = np.mean(bt_bin)
    vect.append(avg_btb)

    # Edge betweenness
    ebt = np.array(nx.edge_betweenness_centrality(graph).values())
    vect.append(np.mean(ebt))

    # Eigen vector centrality binary
    evc_bin = eigenvector_centrality_und(adj_bin)
    avg_evcb = np.mean(evc_bin)
    vect.append(avg_evcb)

    # Flow coefficient
    _, flow_bin, _ = flow_coef_bd(adj_bin)
    avg_flow = np.mean(flow_bin)
    vect.append(avg_flow)

    # Kcoreness centrality
    kcor_bin, _ = kcoreness_centrality_bu(adj_bin)
    avg_kcor = np.mean(kcor_bin)
    vect.append(avg_kcor)

    # Degree assortivity
    dac = nx.degree_assortativity_coefficient(graph)
    vect.append(dac)

    # Page rank centrality
#    pgr_wei = pagerank_centrality(adj_bin, d=0.85)
#    avg_pgr = np.mean(pgr_wei)
#    vect.append(avg_pgr)

    # Rich club coefficient
#    rcc = nx.rich_club_coefficient(graph).values()
#    avg_rcc = np.mean(rcc)
#    vect.append(avg_rcc)

    # Transitivity
    tr = nx.transitivity(graph)
    vect.append(tr)

    # average clustering
    avg_clst = nx.average_clustering(graph)
    vect.append(avg_clst)

    glb_ef = efficiency_bin(adj_bin)
    vect.append(glb_ef)

    return vect


def complex_networks_mapping_uri_data(directory):
    """
    Parameters
    ----------
    directory: string
        The path of the directory containing all data files.
    """

    # Computing the graph encoding
    graphs = []
    classes = []
    subjects = []
    vects = []

    # have 100 graphs already built
    niter = 100
    for subjid in ['pandit', 'ctrl']:
        thresh_dens = '0.1'
        for n in range(niter):
            subj_name = '%s_%d' % (subjid, n)
            g_name = 'iter%d.a.%s.dens_%s.edgelist.gz' % \
                (n, subjid, thresh_dens)
            el = nx.read_edgelist(os.path.join(directory, g_name),
                                  nodetype=int)
            g = nx.Graph()
            # there are 148 regions, or nodes
            g.add_nodes_from(range(148))
            g.add_edges_from(el.edges())
            graphs.append(g)
            subjects.append(subj_name)
            classes.append(subjid)
            vects.append(complex_network_mapping(graphs[-1]))
            print "Graph built for subject %s and class %s." % \
                (subj_name, subjid)

    # Reordering data for the leave-one-subject-out cross-validation
    nm_graphs = [None] * len(graphs)
    nm_classes = [None] * len(classes)
    nm_subjects = [None] * len(subjects)
    nm_vects = [None] * len(vects)

    for i in range(len(graphs) / 2):
        nm_graphs[i*2] = graphs[i]
        nm_graphs[i*2 + 1] = graphs[(len(graphs) / 2) + i]
        nm_classes[i*2] = classes[i]
        nm_classes[i*2 + 1] = classes[(len(classes) / 2) + i]
        nm_subjects[i*2] = subjects[i]
        nm_subjects[i*2 + 1] = subjects[(len(subjects) / 2) + i]
        nm_vects[i*2] = vects[i]
        nm_vects[i*2 + 1] = vects[(len(vects) / 2) + i]

    print nm_subjects
    print nm_classes

    nm_vects = np.array(nm_vects)
#    nm_vects = np.where(nm_vects == inf, 10, nm_vects)
#    nm_vects = np.where(nm_vects == nan, 10, nm_vects)

    ss = StandardScaler()
    X = ss.fit_transform(nm_vects)
    print X
    print np.mean(X)
    print np.max(X)

    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=KFold(len(nm_classes),
                           niter, shuffle=False))
    clf.fit(X, np.array(nm_classes))
    clf.best_params_
    clf = SVC(C=100, kernel='linear')
    print "Now getting cross validation "
    cvr = SVC(C=1000, gamma=.001, kernel='rbf')
    cv_scores = cross_val_score(cvr, X, np.array(nm_classes),
                                cv=KFold(len(nm_classes),
                                         niter, shuffle=False))

    cv_scores = cross_val_score(clf, X, np.array(nm_classes),
                                cv=KFold(len(nm_classes),
                                         niter, shuffle=False))

    clfGD = SGDClassifier()
    cv_scores = cross_val_score(clfGD, X, np.array(nm_classes),
                                cv=KFold(len(nm_classes),
                                         niter, shuffle=False))


    from sklearn.ensemble import ExtraTreesClassifier
    xtc = ExtraTreesClassifier()
    xnew = xtc.fit(X, np.array(nm_classes)).transform(X)
    print xtc.feature_importances_

    ns = cross_val_score(SVC(kernel='linear'), xnew, np.array(nm_classes),
                         cv=KFold(len(nm_classes),
                                  niter, shuffle=False))
    print ns.mean()

    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import RandomForestClassifier
    fp = Pipeline([('feature_selection', LinearSVC(penalty="l2")),
                    ('classification', RandomForestClassifier())])
    fpfit = fp.fit(X, np.array(nm_classes))
    fpfit.score(X, np.array(nm_classes))
#    fpcv = cross_val_score(fpfit, X, np.array(nm_classes),
#                    cv=KFold(len(nm_classes), niter, shuffle=False))
    rf = RandomForestClassifier()
    rf.fit(X, np.array(nm_classes))
    rfx = rf.fit(X, np.array(nm_classes)).transform(X)    


    print cv_scores
    print np.mean(cv_scores)
    print("Accuracy: %0.2f (+/- %0.2f)" %
        (cv_scores.mean(), cv_scores.std() * 2))
