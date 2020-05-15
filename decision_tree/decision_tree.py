from csv import reader
import os

path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                    'data', 'input')


def load_csv(filename):
    file = open(path + filename, "rt")
    lines = reader(file)
    dataset = list(lines)
    return dataset


def find_best_split(data):
    # subset_n = int(math.sqrt(len(data)+1))
    # # exclude 'label' column
    # columns = random.choices(column_name, k=subset_n)

    gini_list = []
    for column in column_name:
        if column != 'label':
            full_col = [x[column] for x in data]
            for feature in list(set(full_col)):
                left_idx, right_idx = data_split(data, column, feature)

                # check if splits are smaller than min_leaf
                left_n = len(left_idx)
                right_n = len(right_idx)
                if left_n == 0 or right_n == 0:
                    pass
                elif left_n > 0 and right_n > 0:
                    left_ratio = left_n / n
                    right_ratio = right_n / n
                    gini = left_ratio * get_gini(filter_row(data, left_idx)) + right_ratio * get_gini(
                        filter_row(data, right_idx))
                    gini_list.append((column, feature, gini))

    if not gini_list:
        return None, None, None
    else:
        return min(gini_list, key=lambda x: x[2])


def filter_row(d, ind):
    index = 0
    filtered_data = []
    for r in d:
        if index in ind:
            filtered_data.append(r)
        index += 1
    return filtered_data


def get_label(data):
    c = {}
    for row in data:
        if row[-1] in c.keys():
            c[row[-1]] += 1
        else:
            c[row[-1]] = 1
    return max(c, key=c.get)


def data_split(data, column, feature):
    left, right = list(), list()
    index = 0
    for row in data:
        if row[column] == feature:
            left.append(index)
        else:
            right.append(index)
        index += 1
    return left, right


def get_gini(data):
    class_column = len(data[0]) - 1
    c = {}
    sum = 0.0
    for row in data:
        if row[class_column] in c.keys():
            c[row[class_column]] += 1
        else:
            c[row[class_column]] = 1
    for k, v in c.items():
        sum = sum + (v / len(data) * v / len(data))
    return 1 - sum

    ## Predict


def predict(data, tree):
    train = data.copy()
    tree_list = [(train, tree)]
    while tree_list:
        train, tree_dict = tree_list.pop(0)

        if tree_dict is not None:

            for key, item in tree_dict.items():
                # if item is not None:
                column, feature, side, number, label = key
                # print(key)

                # on left leaf
                if side == 'left':
                    left_idx, right_idx = data_split(train, column, feature)
                    # add last column as label for this data
                    for it in filter_row(data, left_idx):
                        it[len(column_name) - 1] = label
                    tree_list.append((filter_row(data, left_idx), item))

                # on right leaf
                else:
                    left_idx, right_idx = data_split(train, column, feature)
                    for it in filter_row(data, right_idx):
                        it[len(column_name) - 1] = label
                    tree_list.append((filter_row(data, right_idx), item))

    return 0


def build_tree(data, base_gini):
    # check if all the samples belong to same class
    all_class = []
    for s_data in data:
        all_class.append(s_data[-1])
    if len(set(all_class)) == 1:
        pass
    else:
        column, feature, min_gini = find_best_split(data)
        left_idx, right_idx = data_split(data, column, feature)
        left_label = get_label(filter_row(data, left_idx))
        right_label = get_label(filter_row(data, right_idx))

        tree = {}
        tree[(column, feature, 'left', len(left_idx), left_label)] = build_tree(filter_row(data, left_idx), min_gini)
        tree[(column, feature, 'right', len(right_idx), right_label)] = build_tree(filter_row(data, right_idx),
                                                                                   min_gini)

        return tree


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

tree = build_tree(train_data, base_gini=get_gini(train_data))
pred = predict(test_data, tree)
for item in test_data:
    print(str(item[-1]))



# https://github.com/tonnykwon/Data-Mining