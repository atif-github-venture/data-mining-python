from apyori import apriori
import os

path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                    'data', 'input')

output_path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                           'data', 'output')

records = []

file_name = path + '/apriori_algo_data.txt'
file = open(file_name)
count = 0
for line in file:
    count += 1
    ls = []
    # line = line.strip()
    # line = re.sub(r"\s+", " ", line)
    for item in line.strip().split(';'):
        ls.append(item)
    records.append(ls)

print(count)
association_rules = apriori(records, min_support=0.01)
association_results = list(association_rules)
print(association_results[0])

st = ''
with open(output_path + '/apriori.txt', 'w') as fp:
    for x in association_results:
        lt = []
        for y in x.items:
            lt.append(y)
        lt = ';'.join(lt)
        st = str(int(x.support * count)) + ':' + lt
        fp.write(st + '\n')
fp.close()

# https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python/
