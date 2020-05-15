import math
from collections import Counter
import itertools
import os

path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                    'data', 'input')


def read_data():
    g_tru = []
    pred_clus = []
    with open(path + '/nmi_jaccard.txt') as f:
        for line in f:
            s = line.strip().split(' ')
            g_tru.append(s[0])
            pred_clus.append(s[1])
    f.close()
    return g_tru, pred_clus


def entropy(data):
    count_dict = Counter(data)
    total = len(data)
    H = 0
    for value in count_dict.values():
        p = value / total
        H -= p * math.log(p)
    return H


def mutual_info(cluster_label, truth_label):
    cluster_dict = Counter(cluster_label)
    truth_dict = Counter(truth_label)
    total = len(cluster_label)
    in_label = [(c, t) for c, t in zip(cluster_label, truth_label)]
    in_dict = Counter(in_label)
    I = 0
    for k, v in in_dict.items():
        c, t = k
        pij = v / total
        pc = cluster_dict[c] / total
        pt = truth_dict[t] / total
        I += pij * math.log(pij / (pc * pt))
    return I


def normal_mut_info(cluster_label, truth_label):
    I = mutual_info(cluster_label, truth_label)
    hc = entropy(cluster_label)
    ht = entropy(truth_label)
    return I / math.sqrt(hc * ht)


def jaccard_sim(cluster_label, truth_label):
    n11 = n10 = n01 = 0
    n = len(cluster_label)
    for i, j in itertools.combinations(range(n), 2):
        c01 = cluster_label[i] == cluster_label[j]
        c02 = truth_label[i] == truth_label[j]
        if c01 and c02:
            n11 += 1
        elif c01 and not c02:
            n10 += 1
        elif not c01 and c02:
            n01 += 1
    return float(n11) / (n11 + n10 + n01)


#################################################################################################
# start algorithm
N = 0
K = 0
M = 0

debug = 1

gr_truth = []
pred_cluster = []
if debug == 1:
    gr_truth, pred_cluster = read_data()
elif debug == 0:
    for i in range(0, 5):
        a = input().split(' ')
        gr_truth.append(a[0])
        pred_cluster.append(a[1])
    while True:
        try:
            a = input().split(' ')
            gr_truth.append(a[0])
            pred_cluster.append(a[1])
        except:
            break

nmi = format(normal_mut_info(pred_cluster, gr_truth), '.3f')
j_sim = format(jaccard_sim(pred_cluster, gr_truth), '.3f')

print(str(nmi) + ' ' + str(j_sim))

# data
# 2 3
# 0 0
# 0 1
# 1 1
# 2 2
