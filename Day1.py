from aocd import *
from sortedcontainers import SortedList
from time import perf_counter
import re

data_input = get_data(day=1, year=2024)
# data_input = "3   4\n4   3\n2   5\n1   3\n3   9\n3   3" # Test input

# Processing data
list1 = SortedList()
list2 = SortedList()
count_dict = dict()

t1_start = perf_counter()

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
t1_stop = perf_counter()

print('Part A - Answer: ' + str(ex1_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(ex1_res, part='a', day=1, year=2024)

# Exercise 2
t2_start = perf_counter()
ex2_res = 0
for el1 in list1_set:
    if el1 in count_dict.keys():
        ex2_res += el1 * count_dict[el1]

t2_stop = perf_counter()
print('Part B - Answer: ' + str(ex2_res) + ', calculated in ' + str((t2_stop - t2_start) * 1000) + ' ms')
submit(ex2_res, part='b', day=1, year=2024)
