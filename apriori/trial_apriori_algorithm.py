from collections import defaultdict
import itertools
from functools import reduce
import os


path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                    'data', 'input')

output_path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                           'data', 'output')


def filter_above_minsup(dict, minsup_threshold):
    c = {}
    local_dict = {k: v for k, v in dict.items() if v >= minsup_threshold}
    di = sorted(local_dict.items(), key=lambda item: item[1])
    for k, v in di:
        c[k] = v
    return c


def write_to_txt(dict, file_name):
    with open(file_name, 'w') as fp:
        for k, v in dict.items():
            if isinstance(k, frozenset):
                st = []
                for x in k:
                    st.append(x)
                fp.write(str(v) + ':' + ';'.join(st) + '\n')
            else:
                fp.write(str(v) + ':' + k + '\n')
    fp.close()


def generate_combinations(ls, length):
    perm = itertools.permutations(ls, 2)
    set_list = []
    for i in list(perm):
        lt = []
        for x in i:
            lt.append(x)
        lt.sort()
        set_list.append(lt)
    set_list.sort()
    new_num = list(set_list for set_list, _ in itertools.groupby(set_list))
    return new_num


def has_infrequent_subset(l, li):
    if len(li) <= 2:
        return True
    else:
        st = []
        for x in li:
            st.append(x)
        gen_list = generate_combinations(st, len(st) - 1)
        for item in gen_list:
            if frozenset(item) not in l:
                return False
    return True


def apriori_gen(l):
    list = []
    for i in range(0, len(l)):
        for j in range(i + 1, len(l)):
            li = []
            li.append(l[i])
            li.append(l[j])
            # flatten it
            ls = []
            for x in li:
                if isinstance(x, frozenset):
                    for y in x:
                        ls.append(y)
                else:
                    break
            if len(ls) > 0:
                li = set(ls)
            if has_infrequent_subset(l, li):
                list.append(set(li))
    return list


def all_item_in_transaction(candidate, line):
    for x in candidate:
        if x not in line:
            return False
    return True


def count_transactions(l, filename):
    c = {}
    for candi in l:
        c[frozenset(candi)] = 0
        file = open(filename)
        for line in file:
            if all_item_in_transaction(candi, line):
                c[frozenset(candi)] += 1
        file.close()
    return c


# ******************************************************************
minsup = 771
c1 = {}
file_name = path + '/apriori_algo_data.txt'
file = open(file_name)
for line in file:
    for item in line.strip().split(';'):
        if item in c1:
            c1[item] += 1
        else:
            c1[item] = 1
file.close()
c1 = filter_above_minsup(c1, minsup)
write_to_txt(c1, output_path + '/patterns.txt')
l = list(c1.keys())
l.sort()

k = 2
while len(l) != 0:
    l = apriori_gen(l)
    trans = count_transactions(l, file_name)
    c1 = filter_above_minsup(trans, minsup)
    write_to_txt(c1, output_path + '/patterns' + str(k) + '.txt')
    l = list(c1.keys())
    print('x')
    k += 1
