from csv import reader
import os

path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                    'data', 'input')


def load_csv(filename):
    file = open(path + filename, "rt")
    lines = reader(file)
    dataset = list(lines)
    return dataset


def test_split(index, value, dataset):
    left, right = list(), list()
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right


# Calculate the Gini index for a split dataset
def gini_index(groups, classes):
    # count all samples at split point
    n_instances = float(sum([len(group) for group in groups]))
    # sum weighted Gini index for each group
    gini = 0.0
    for group in groups:
        size = float(len(group))
        # avoid divide by zero
        if size == 0:
            continue
        score = 0.0
        # score the group based on the score for each class
        for class_val in classes:
            p = [row[-1] for row in group].count(class_val) / size
            score += p * p
        # weight the group score by its relative size
        gini += (1.0 - score) * (size / n_instances)
    return gini


# Select the best split point for a dataset
def get_split(dataset):
    class_values = list(set(row[-1] for row in dataset))
    b_index, b_value, b_score, b_groups = 999, 999, 999, None
    for index in range(len(dataset[0]) - 1):
        for row in dataset:
            groups = test_split(index, row[index], dataset)
            gini = gini_index(groups, class_values)
            if gini < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    return {'index': b_index, 'value': b_value, 'groups': b_groups}


# Create a terminal node value
def to_terminal(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)


# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth):
    left, right = node['groups']
    del (node['groups'])
    # check for a no split
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        return
    # check for max depth
    if depth >= max_depth:
        node['left'], node['right'] = to_terminal(left), to_terminal(right)
        return
    # process left child
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
    else:
        node['left'] = get_split(left)
        split(node['left'], max_depth, min_size, depth + 1)
    # process right child
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
    else:
        node['right'] = get_split(right)
        split(node['right'], max_depth, min_size, depth + 1)


# Build a decision tree
def build_tree(train, max_depth, min_size):
    root = get_split(train)
    split(root, max_depth, min_size, 1)
    return root


# # Print a decision tree
# def print_tree(node, depth=0):
#     if isinstance(node, dict):
#         print('%s[X%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
#         print_tree(node['left'], depth+1)
#         print_tree(node['right'], depth+1)
#     else:
#         print('%s[%s]' % ((depth*' ', node)))

def predict(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']


debug = 1
dataset = []
dataset_test = []
if debug == 1:
    filename = '/decisiontree_training.txt'
    filename_test = '/decisiontree_testing.txt'
    dataset = load_csv(filename)
    dataset_test = load_csv(filename_test)

elif debug == 0:
    iteration = input()
    for i in range(0, int(iteration)):
        dataset.append(input())
    iteration = input()
    for i in range(0, int(iteration)):
        dataset_test.append(input())

count = 0
column_name = []
train_data = []
test_data = []
for it in dataset:
    if debug == 0:
        i_split = it.split(' ')
    else:
        i_split = it[0].split(' ')
    if count == 0:
        # set column names
        for i in range(1, len(i_split)):
            column_name.append(int(i_split[i].split(':')[0]))
        column_name.append('label')
        count = + 1
    row = []
    for i in range(1, len(i_split)):
        row.append(int(i_split[i].split(':')[1]))
    row.append(int(i_split[0]))
    train_data.append(row)
n = len(train_data)

for it in dataset_test:
    if debug == 0:
        i_split = it.split(' ')
    else:
        i_split = it[0].split(' ')
    # i_split.append('0:0')
    row = []
    for i in range(0, len(i_split)):
        row.append(int(i_split[i].split(':')[1]))
    test_data.append(row)

tree = build_tree(train_data, 4, 1)
for id in test_data:
    print(predict(tree, row=id))


# https://machinelearningmastery.com/implement-decision-tree-algorithm-scratch-python/
# https://github.com/Lieu98/Decision_tree/blob/master/gini_index.py