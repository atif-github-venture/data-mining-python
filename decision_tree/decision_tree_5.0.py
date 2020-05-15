from __future__ import print_function
from csv import reader

import os

path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                    'data', 'input')


def load_csv(filename):
    file = open(path + filename, "rt")
    lines = reader(file)
    dataset = list(lines)
    return dataset


def class_counts(rows):
    counts = {}
    for row in rows:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)


class Check:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the check in a readable format.
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))


def partition(rows, check):
    true_rows, false_rows = [], []
    for row in rows:
        if check.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl ** 2
    return impurity


def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


def find_best_split(rows):
    best_gain = 0
    best_check = None
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1

    for col in range(n_features):
        values = set([row[col] for row in rows])
        for val in values:
            check = Check(col, val)
            true_rows, false_rows = partition(rows, check)
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            gain = info_gain(true_rows, false_rows, current_uncertainty)
            if gain >= best_gain:
                best_gain, best_check = gain, check
    return best_gain, best_check


class Leaf:
    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:
    def __init__(self,
                 check,
                 true_branch,
                 false_branch):
        self.check = check
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):
    gain, check = find_best_split(rows)
    if gain == 0:
        return Leaf(rows)

    true_rows, false_rows = partition(rows, check)
    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)
    return Decision_Node(check, true_branch, false_branch)


def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions

    if node.check.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


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
n = float(len(train_data))

for it in dataset_test:
    if debug == 0:
        i_split = it.split(' ')
    else:
        i_split = it[0].split(' ')
    i_split.append('0:0')
    row = []
    for i in range(0, len(i_split)):
        row.append(int(i_split[i].split(':')[1]))
    test_data.append(row)

header = column_name

my_tree = build_tree(train_data)
# print(classify(training_data[0], my_tree))
for row in test_data:
    for k, v in classify(row, my_tree).items():
        print(k)


# https://github.com/random-forests/tutorials/blob/master/decision_tree.ipynb
# https://www.youtube.com/watch?v=LDRbO9a6XPU