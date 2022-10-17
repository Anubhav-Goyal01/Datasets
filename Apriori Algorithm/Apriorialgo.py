import sys
from pyreadline3 import Readline
import itertools
import tracemalloc
tracemalloc.start()
min_support = sys.argv[2]
min_confidence = sys.argv[3]
with open(sys.argv[1], 'r') as filedata:
    read_lines = filedata.readlines()
arr_itemset = []


def item_set1():
    count = {}
    count1 = []
    for data_items in read_lines:
        data_items = data_items.strip()
        data_split = data_items.split(",")
        arr_itemset.append(data_split)
        for dataItem in data_split:
            if dataItem not in count:
                count[(dataItem)] = 1
            else:
                count[(dataItem)] += 1
    for a in count:
        if count[a] >= float(min_support)*len(read_lines):
            count1.append(a)
    return count1, count


def item_set(Length1, c, k):
    itemset_length1 = []
    if (c == 1):
        for i in range(len(Length1)):
            for j in range(i+1, len(Length1)):
                c = []
                c.append(Length1[i])
                c.append(Length1[j])
                if c not in itemset_length1:
                    itemset_length1.append(c)

    else:
        for i in range(len(Length1)):
            for j in range(i+1, len(Length1)):

                l = list(set(Length1[i] + Length1[j]))
                if len(l) == k:
                    if sorted(l) not in itemset_length1:
                        itemset_length1.append(sorted(l))

    return itemset_length1


def freq_itemsets(length, length_1, n):
    count = []
    count1 = {}
    final_itemset1 = []
    for x in length:
        c = 0
        freq_len1 = set(itertools.combinations(x, n))
        for item in freq_len1:
            if set(item).issubset(set(length_1)):
                c += 1
        if c == len(freq_len1):
            count.append(x)

    for item in count:
        c = 0
        for x in arr_itemset:
            if (set(item).issubset(set(x))):
                c += 1
        count1[tuple(item)] = c

    for item in count1:
        if count1[tuple(item)] >= float(min_support)*len(read_lines):
            if item not in final_itemset1:
                final_itemset1.append(item)

    return final_itemset1


def freq_itemsets2(length, length1, n):
    count = []
    count2 = {}
    final_itemset2 = []
    for x in length:
        c = 0
        combo_list = set(itertools.combinations(x, n))
        for item in combo_list:
            flag = 0
            for element in length1:
                if set(element) == set(item):
                    flag = 1
                    break
            if flag == 1:
                c += 1

        if c == len(combo_list):
            if sorted(x) not in count:
                count.append(sorted(x))

    for item in count:
        c = 0
        for x in arr_itemset:
            if (set(item).issubset(set(x))):
                c += 1
        count2[tuple(item)] = c
    for item in count2:
        if count2[tuple(item)] >= float(min_support)*len(read_lines):
            final_itemset2.append(item)

    return final_itemset2


def generate_rules(frequent_items):
    for x in frequent_items:
        c = 0
        for data in arr_itemset:
            if (set(x).issubset(set(data))):
                c += 1
        union_min_support = c
        min_support = union_min_support/len(read_lines)
        sub_set = []
        length = len(x)
        for i in range(1, length):
            combo_list = set(itertools.combinations(x, i))
            sub_set += sorted(combo_list)
        for i in sub_set:
            left = i
            right = set(x) - set(i)
            c = 0
            for data in arr_itemset:
                if (set(left).issubset(set(data))):
                    c += 1
            pre_min_confidence = union_min_support/c
            answer = "{"
            if pre_min_confidence >= float(min_confidence):
                j = 0
                for i in list(left):
                    if j == 1:
                        answer += ','
                    answer += i.strip()
                    j = 1
                answer += '}{'
                for i in list(right):
                    if j == 0:
                        answer += ','
                    answer += i.strip()
                    j = 0
                answer = answer + '}[' + str(min_support) + ',' + \
                    "{:.4f}".format(pre_min_confidence) + ']'
                print(answer)


def apriori():
    L1, L1map = item_set1()
    freq_items = L1
    Length1 = L1
    prefinal_itemset = []
    k = 2
    while len(freq_items):
        prefinal_itemset = freq_items
        if k == 2:
            freq_items = item_set(freq_items, 1, k)
            freq_items = freq_itemsets(freq_items, Length1, k-1)
            Length1 = freq_items

        else:
            freq_items = item_set(freq_items, 0, k)
            freq_items = freq_itemsets2(freq_items, Length1, k-1)
            Length1 = freq_items
        k += 1
    generate_rules(prefinal_itemset)


apriori()
print(tracemalloc.get_traced_memory())
tracemalloc.stop()
