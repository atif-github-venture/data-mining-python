from nltk import word_tokenize
from nltk.util import ngrams
import os


path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                    'data', 'input')

output_path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                           'data', 'output')


def get_ngrams(text, n):
    n_grams = ngrams(word_tokenize(text), n)
    return [' '.join(grams) for grams in n_grams]


def drop_seq_if_infrequent(sequ, singitemset):
    pruned_seq = list()
    for s in sequ:
        state = True
        arr = s.split()
        for x in arr:
            if x not in singitemset:
                state = False
                break
        if state:
            pruned_seq.append(s)
    return pruned_seq


def drop_dict_if_less_sup(dic, sup):
    s = ''
    for a, b in dic.items():
        if b >= sup:
            s = s + '{}:{}\n'.format(b, a.replace(' ', ';'))
    return s


def count_transactions(l, filename, size):
    c = dict.fromkeys(l, 0)
    file = open(filename)
    for li in file:
        smallset = set(get_ngrams(li.strip(), size))
        for y in smallset:
            if y in c:
                c[y] += 1
    file.close()
    return c


file_name = path + '/reviews_sample.txt'
full_list = []
support = 100

# find frequent-1 itemset per given support
file = open(file_name)
c1 = {}
strg = ''
for line in file:
    # set the list so that repetitive items dont increase count
    p = set(line.strip().split())
    for item in p:
        if item in c1:
            c1[item] += 1
        else:
            c1[item] = 1
print(c1)
file.close()
d1 = {}
above_sup_single_item_set = []
for k, v in c1.items():
    if v >= 100:
        d1[k] = v
        strg = strg + '{}:{}\n'.format(v, k)
        above_sup_single_item_set.append(k)

# form sequential words for n length and have them as list of set
for n in range(2, 4):
    li_ngram = []
    file = open(file_name)
    for line in file:
        seq = get_ngrams(line.strip(), n)
        seq = drop_seq_if_infrequent(seq, above_sup_single_item_set)
        for item in seq:
            li_ngram.append(item)
    file.close()
    li_ngram = count_transactions(set(li_ngram), file_name, n)
    strg = strg + drop_dict_if_less_sup(li_ngram, support)

with open(output_path + '/patterns.txt', 'w') as fp:
    fp.write(strg)
fp.close()

print('done')

# give the "" around the text line
# try with r studio on MAC
# library(CSeqpat)
# CSeqpat("/Users/atifahmed/Documents/git_projects/cs412-data-mining-assignments/data/reviews_sample.txt", minsupport=100, docdelim=' ')
