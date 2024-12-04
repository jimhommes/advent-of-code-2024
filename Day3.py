from aocd import *
import re
import math
import itertools

data_input = re.sub('\n', '', get_data(day=3, year=2024))
# data_input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

ex1_res = sum([math.prod(list(map(int, re.findall(r'\d+', x)))) for x in re.findall(r'mul\(\d+,\d+\)', data_input)])
print(ex1_res)
submit(ex1_res, part='a', day=3, year=2024)

mls = list(itertools.chain.from_iterable([re.findall(r'mul\(\d+,\d+\)', x) for x in re.findall(r"^.*?don't\(\)|do\(\).*?don't\(\)|do\(\).*?$", data_input)]))
ex2_res = sum([math.prod(list(map(int, re.findall(r'\d+', x)))) for x in mls])
print(ex2_res)
submit(ex2_res, part='b', day=3, year=2024)
