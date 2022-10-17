import csv
import itertools
import math
import sys
import tracemalloc

data_file = open(sys.argv[1], 'r')
min_support = float(sys.argv[2])
min_confidence = float(sys.argv[3])


def item_set1():
    read_data = csv.reader(data_file, delimiter=',')
    dataset = list(read_data)
    trans_list = []
    for e in dataset:
        arr_list = []
        for i in e:
            arr_list.append(str(i).lstrip().rstrip())
        trans_list.append(sorted(arr_list))
    dataset = trans_list
    item_count = {}
    for items in dataset:
        for item in items:
            if item not in item_count:
                item_count[(item)] = 1
            else:
                item_count[(item)] = item_count[(item)] + 1
    count2 = {k: v for k, v in item_count.items() if v >=
              math.ceil(min_support*len(dataset))}
    return count2, dataset


def combination_generator(Length1, data_flag, data):
    Combo = []
    if data_flag == 1:
        data_flag = 0
        for item1 in Length1:
            for item2 in Length1:
                if item2 > item1:
                    Combo.append((item1, item2))
    else:
        for item in Length1:
            k = len(item)
        for item1 in Length1:
            for item2 in Length1:
                if (item1[:-1] == item2[:-1]) and (item1[-1] != item2[-1]):
                    if item1[-1] > item2[-1]:
                        Combo.append(item2 + (item1[-1],))
                    else:
                        Combo.append(item1 + (item2[-1],))
    L = freq_itemset(set(Combo), data)
    return L, data_flag


def freq_itemset(Combo, data):
    count = {}
    for itemset in Combo:
        for action_list in data:
            if all(e in action_list for e in itemset):
                if itemset not in count:
                    count[itemset] = 1
                else:
                    count[itemset] = count[itemset] + 1

    count2 = {k: v for k, v in count.items() if v >=
              math.ceil(min_support*len(data))}
    return count2


def generate_rules(frequent_itemset, data):
    for itemset in frequent_itemset.keys():
        if isinstance(itemset, str):
            continue
        length = len(itemset)
        SupportUnion = frequent_itemset[tuple(itemset)]
        for i in range(1, length):
            left_set = map(list, itertools.combinations(itemset, i))
            for left in left_set:
                if len(left) == 1:
                    if ''.join(left) in frequent_itemset:
                        count_of_left = frequent_itemset[''.join(left)]
                        confidence = SupportUnion / count_of_left
                else:
                    if tuple(left) in frequent_itemset:
                        count_of_left = frequent_itemset[tuple(left)]
                        confidence = SupportUnion / count_of_left
                if confidence >= min_confidence:
                    right = list(itemset[:])
                    for e in left:
                        right.remove(e)
                    print('{'+str(','.join(left)).strip() + '}' + '{' + ','.join(right) +
                          '}' + '[' + str(SupportUnion/len(data)) + ',' + str(round(confidence, 4))+']')


def pcy_hashalgo():
    L, data = item_set1()
    data_flag = 1
    hash_table = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in data:
        combination_sett = list(itertools.combinations(i, 2))
        for j in combination_sett:
            x = j[0]
            y = j[1]
            x = int(x.replace('I', ''))
            y = int(y.replace('I', ''))
            index = (x+y)*(x-y) % 9
            hash_table[index] += 1
    f2itemset = {}
    for combination in itertools.combinations(L, 2):
        x = combination[0]
        y = combination[1]
        x = int(x.replace('I', ''))
        y = int(y.replace('I', ''))
        index = (x+y)*(x-y) % 9
        if hash_table[index] >= math.ceil(min_support*len(data)):
            f2itemset[combination] = 0
    for i in data:
        for j in f2itemset.keys():
            if j[0] in i and j[1] in i:
                f2itemset[j] += 1
    FreqItems = dict(L)
    FreqItems.update(f2itemset)
    while (len(L) != 0):
        L, data_flag = combination_generator(L, data_flag, data)
        FreqItems.update(L)
    generate_rules(FreqItems, data)


if __name__ == '__main__':
    tracemalloc.start()
    pcy_hashalgo()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    # print(current_memory)
