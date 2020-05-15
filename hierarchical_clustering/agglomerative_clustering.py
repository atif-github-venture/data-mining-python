import math
import os

path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                    'data', 'input')


def distance(vc1, vc2, minmax):
    if len(vc1) == 2 and len(vc2) == 2:
        return euclidean_distance(vc1, vc2)
    else:
        a = form_pair(vc1)
        b = form_pair(vc2)
        local_dis = []
        for x in a:
            for y in b:
                local_dis.append(euclidean_distance(x, y))
        if minmax == 'min':
            return min(local_dis)
        elif minmax == 'max':
            return max(local_dis)
        elif minmax == 'avg':
            return sum(local_dis) / len(local_dis)
        print('done')


def euclidean_distance(vc1, vc2):
    calc = math.sqrt((vc1[0] - vc2[0]) ** 2 + (vc1[1] - vc2[1]) ** 2)
    return calc


def form_pair(it):
    cnt = 0
    ap = []
    for i in range(0, int(len(it) / 2)):
        ap.append([it[i + cnt], it[i + 1 + cnt]])
        cnt += 1
    return ap


def read_data():
    inp = []
    with open(path + '/places_aggloclus.txt') as f:
        for line in f:
            lst = []
            for x in line.strip().split(' '):
                try:
                    lst.append(int(x))
                except ValueError as e:
                    lst.append(float(x))
            inp.append(lst)
    f.close()
    return inp


def average_link(clusters, cluster_num):
    while len(clusters) is not cluster_num:
        closest_distance = clust_1 = clust_2 = math.inf
        for cluster_id, cluster in enumerate(clusters[:len(clusters)]):
            for cluster2_id, cluster2 in enumerate(clusters[(cluster_id + 1):]):
                dis = distance(cluster, cluster2, 'avg')
                if dis < closest_distance:
                    closest_distance = dis
                    clust_1 = cluster_id
                    clust_2 = cluster2_id + cluster_id + 1
        clusters[clust_1].extend(clusters[clust_2])
        clusters.pop(clust_2)
    return clusters


def complete_link(clusters, cluster_num):
    while len(clusters) is not cluster_num:
        closest_distance = clust_1 = clust_2 = math.inf
        for cluster_id, cluster in enumerate(clusters[:len(clusters)]):
            for cluster2_id, cluster2 in enumerate(clusters[(cluster_id + 1):]):
                dis = distance(cluster, cluster2, 'max')
                if dis < closest_distance:
                    closest_distance = dis
                    clust_1 = cluster_id
                    clust_2 = cluster2_id + cluster_id + 1
        clusters[clust_1].extend(clusters[clust_2])
        clusters.pop(clust_2)
    return clusters


def single_link(clusters, cluster_num):
    while len(clusters) is not cluster_num:
        closest_distance = clust_1 = clust_2 = math.inf
        for cluster_id, cluster in enumerate(clusters[:len(clusters)]):
            for cluster2_id, cluster2 in enumerate(clusters[(cluster_id + 1):]):
                dis = distance(cluster, cluster2, 'min')
                if dis < closest_distance:
                    closest_distance = dis
                    clust_1 = cluster_id
                    clust_2 = cluster2_id + cluster_id + 1
        clusters[clust_1].extend(clusters[clust_2])
        clusters.pop(clust_2)
    return clusters


def hierarchical_clustering(data, cluster_num, measure=0):
    init_clusters = [data[i] for i in range(len(data))]
    if measure == 0:
        return single_link(init_clusters, cluster_num)
    if measure == 1:
        return complete_link(init_clusters, cluster_num)
    if measure == 2:
        return average_link(init_clusters, cluster_num)


#################################################################################################
# start algorithm
N = 0
K = 0
M = 0

debug = 1
input_data = []
if debug == 1:
    N = 5
    K = 2
    M = 2
    input_data = read_data()
elif debug == 0:
    config = input()
    N = int(config.split(' ')[0])
    K = int(config.split(' ')[1])
    M = int(config.split(' ')[2])
    # print(str(N) + str(K) + str(M))
    for i in range(0, N):
        a = input()
        input_data.append([float(a.split(' ')[0]), float(a.split(' ')[1])])
    # for it in input_data:
    #     print(it)

cal_clust = hierarchical_clustering(input_data, K, M)
lst = []
for item in cal_clust:
    ap = form_pair(item)
    lst.append(ap)
for idx, item in enumerate(lst):
    for it in item:
        print(idx)

# https://medium.com/@rohanjoseph_91119/learn-with-an-example-hierarchical-clustering-873b5b50890c
