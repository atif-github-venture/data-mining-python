# got score 5 out of 5

import fileinput


def distance(x, y, m):
    dist = [(x[idx] - y[idx]) ** 2 for idx in range(len(x) - 1)]
    return sum(dist) ** (1 / 2)


def cluster_dist(item1, item2, m):
    dist_list = [dist_mat[element1][element2] for element1 in item1 for element2 in item2 if element1 != element2]
    if dist_list:
        if m == 0:
            temp = min(dist_list)
        elif m == 1:
            temp = max(dist_list)
        else:
            temp = sum(dist_list) / len(dist_list)
        return temp


inputdata = dict()
idx = 0
for line in fileinput.input():
    if fileinput.isfirstline():
        n, k, m = line.split(' ')
        k = int(k)
        n = int(n)
        m = int(m)
    else:
        lon, lat = line.split(' ')
        inputdata.update({idx: [float(lon), float(lat), idx]})
        idx += 1

# calculate distance matrix
dist_mat = [[float('inf') for i in range(n)] for j in range(n)]
for i in inputdata.keys():
    for j in inputdata.keys():
        if i != j:
            dist_mat[i][j] = distance(inputdata.get(i), inputdata.get(j), m)

# make cluster dictionary
cluster_dict = dict()
[cluster_dict.update({key: [key]}) for key in inputdata.keys()]

# Repeat merging until getting k clusters
while n > k:
    # calculate distance between clusters
    sorted_keys = sorted(list(cluster_dict.keys()))
    dist_list = [(key1, key2, cluster_dist(cluster_dict.get(key1), cluster_dict.get(key2), m)) for idx1, key1 in
                 enumerate(sorted_keys)
                 for idx2, key2 in enumerate(sorted_keys[idx1 + 1:])]
    # dist_list= [(key1, key2, cluster_dist(item1, item2, m)) for key1, item1 in cluster_dict.items()
    #            for key2, item2 in cluster_dict.items() if key1!=key2]
    i, j, _ = min(dist_list, key=lambda t: t[2] if t[2] else float('inf'))

    # get new cluster and remove previous ones
    new_cluster = cluster_dict.get(i) + cluster_dict.get(j)
    temp = cluster_dict.pop(i)
    temp = cluster_dict.pop(j)
    cluster_dict.update({i: new_cluster})

    # update cluster list
    new_cluster_dict = dict()
    idx = 0
    for key, item in cluster_dict.items():
        new_cluster_dict.update({idx: item})
        idx += 1
    cluster_dict = new_cluster_dict

    n = len(cluster_dict)

# print out results after transforming to list
result_list = [[key, element] for key, item in cluster_dict.items() for element in item]
arg_sort_idx = sorted(range(len(result_list)), key=list(zip(*result_list))[1].__getitem__)
clusters = list(zip(*result_list))[0]

for idx in arg_sort_idx:
    print(clusters[idx])
