from aocd import *
from sortedcontainers import SortedList
import re

data_input = get_data(day=1, year=2024)
# data_input = "3   4\n4   3\n2   5\n1   3\n3   9\n3   3" # Test input

list1 = SortedList()
list2 = SortedList()

for line in data_input.split('\n'):
    numbers = re.findall(r'\d+', line)
    list1.add(int(numbers[0]))
    list2.add(int(numbers[1]))

distancelist = [abs(x - y) for (x, y) in zip(list1, list2)]
distancesum = sum(distancelist)
print(distancesum)
submit(distancesum, part='a', day=1, year=2024)
