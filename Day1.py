from aocd import *
from sortedcontainers import SortedList
import re

data_input = get_data(day=1, year=2024)
# data_input = "3   4\n4   3\n2   5\n1   3\n3   9\n3   3" # Test input

# Processing data
list1 = SortedList()
list2 = SortedList()
count_dict = dict()

for line in data_input.split('\n'):
    numbers = re.findall(r'\d+', line)
    list1.add(int(numbers[0]))
    list2.add(int(numbers[1]))

    if int(numbers[1]) not in count_dict.keys():
        count_dict[int(numbers[1])] = 1
    else:
        count_dict[int(numbers[1])] += 1

list1_set = set(list1)

# Exercise 1
distancelist = [abs(x - y) for (x, y) in zip(list1, list2)]
ex1_res = sum(distancelist)
print(ex1_res)
submit(ex1_res, part='a', day=1, year=2024)

# Exercise 2
ex2_res = 0
for el1 in list1_set:
    if el1 in count_dict.keys():
        ex2_res += el1 * count_dict[el1]

print(ex2_res)
submit(ex2_res, part='b', day=1, year=2024)
