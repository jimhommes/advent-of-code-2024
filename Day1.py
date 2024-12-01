from aocd import *
from sortedcontainers import SortedList
import re

data_input = get_data(day=1, year=2024)
# data_input = "3   4\n4   3\n2   5\n1   3\n3   9\n3   3" # Test input

# Processing data
list1 = SortedList()
list2 = SortedList()

for line in data_input.split('\n'):
    numbers = re.findall(r'\d+', line)
    list1.add(int(numbers[0]))
    list2.add(int(numbers[1]))

# Exercise 1
distancelist = [abs(x - y) for (x, y) in zip(list1, list2)]
ex1_res = sum(distancelist)
print(ex1_res)
submit(ex1_res, part='a', day=1, year=2024)

# Exercise 2
count_dict = dict()
ex2_res = 0
while len(list1) > 0:
    el1 = list1.pop()
    if el1 in count_dict.keys():
        ex2_res += el1 * count_dict[el1]
    else:
        el2 = list2.pop()
        while el2 > el1:
            el2 = list2.pop()
        count = 0
        while el2 == el1:
            count += 1
            el2 = list2.pop()
        list2.add(el2)
        ex2_res += el1 * count
        count_dict[el1] = count

print(ex2_res)
submit(ex2_res, part='b', day=1, year=2024)
