from aocd import *
from time import perf_counter
import re
import math
import itertools

data_input = re.sub('\n', '', get_data(day=3, year=2024))
# data_input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

t1_start = perf_counter()
ex1_res = sum([math.prod(list(map(int, re.findall(r'\d+', x)))) for x in re.findall(r'mul\(\d+,\d+\)', data_input)])
t1_stop = perf_counter()
print('Part A - Answer: ' + str(ex1_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(ex1_res, part='a', day=3, year=2024)

t2_start = perf_counter()
mls = list(itertools.chain.from_iterable([re.findall(r'mul\(\d+,\d+\)', x) for x in re.findall(r"^.*?don't\(\)|do\(\).*?don't\(\)|do\(\).*?$", data_input)]))
ex2_res = sum([math.prod(list(map(int, re.findall(r'\d+', x)))) for x in mls])
t2_stop = perf_counter()
print('Part B - Answer: ' + str(ex2_res) + ', calculated in ' + str((t2_stop - t2_start) * 1000) + ' ms')
submit(ex2_res, part='b', day=3, year=2024)
