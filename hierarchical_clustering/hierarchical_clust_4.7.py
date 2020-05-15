import sys
import math
import os

path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                    'data', 'input')


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


def pairwise_distances(d):
    mat = []
    for z in range(0, len(d)):
        row = []
        for j in range(0, len(d)):
            row.append(euclidean_distance(d[z], d[j]))
        mat.append(row)
    return mat


def euclidean_distance(vc1, vc2):
    return math.sqrt((vc1[0] - vc2[0]) ** 2 + (vc1[1] - vc2[1]) ** 2)


def fill_diagonal(matr, va):
    for z in range(0, len(matr)):
        for j in range(0, len(matr)):
            if z == j:
                matr[z][j] = va
    return matr


def hierarchical_clustering(data, linkage):
    initial_distances = pairwise_distances(data)
    initial_distances = fill_diagonal(initial_distances, sys.maxsize)
    clus = find_clusters(initial_distances, linkage)
    return clus


def find_clusters(input, linkage):
    clusters = {}
    row_index = -1
    col_index = -1
    array = []

    for n in range(len(input)):
        array.append(n)

    clusters[0] = array.copy()
    for k in range(1, len(input)):
        min_val = sys.maxsize

        for i in range(0, len(input)):
            for j in range(0, len(input[0])):
                if input[i][j] <= min_val:
                    min_val = input[i][j]
                    row_index = i
                    col_index = j

        if linkage == "single":
            for i in range(0, len(input)):
                if i != col_index:
                    temp = min(input[col_index][i], input[row_index][i])
                    input[col_index][i] = temp
                    input[i][col_index] = temp
        elif linkage == "complete":
            for i in range(0, len(input)):
                if i != col_index and i != row_index:
                    temp = max(input[col_index][i], input[row_index][i])
                    input[col_index][i] = temp
                    input[i][col_index] = temp
        elif linkage == "average":
            for i in range(0, len(input)):
                if i != col_index and i != row_index:
                    temp = ((input[col_index][i] + input[row_index][i]) / 2)
                    input[col_index][i] = temp
                    input[i][col_index] = temp

        for i in range(0, len(input)):
            input[row_index][i] = sys.maxsize
            input[i][row_index] = sys.maxsize

        minimum = min(row_index, col_index)
        maximum = max(row_index, col_index)
        for n in range(len(array)):
            if array[n] == maximum:
                array[n] = minimum
        clusters[k] = array.copy()

    return clusters


#################################################################################################
# start algorithm
N = 0
K = 0
M = 0

debug = 1
input_data = []
if debug == 1:
    N = 5
    K = 1
    M = 2
    input_data = read_data()
elif debug == 0:
    config = input()
    N = int(config.split(' ')[0])
    K = int(config.split(' ')[1])
    M = int(config.split(' ')[2])
    while True:
        try:
            a = input()
            input_data.append([float(a.split(' ')[0]), float(a.split(' ')[1])])
        except:
            break

link = None
if M == 0:
    link = 'single'
if M == 1:
    link = 'complete'
if M == 2:
    link = 'average'
cluster_s = hierarchical_clustering(input_data, link)
for loop in cluster_s[len(cluster_s) - K]:
    print(loop)

# data
# 5 2 0
# 51.5217 30.1140
# 27.9698 27.0568
# 10.6233 52.4207
# 122.1483 6.9586
# 146.4236 -41.3457
