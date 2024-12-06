from aocd import *
from time import perf_counter
import numpy as np

data_input = get_data(day=5, year=2024).split('\n\n')
rules_lines = data_input[0].split('\n')
update_lines = data_input[1].split('\n')
rules = dict()

for rule_line in rules_lines:
    spl = rule_line.split('|')
    if int(spl[0]) not in rules.keys():
        rules[int(spl[0])] = [int(spl[1])]
    else:
        rules[int(spl[0])].append(int(spl[1]))

ex1_res = 0
t1_start = perf_counter()
for update_line in update_lines:
    spl = np.array(update_line.split(',')).astype(int)
    line_valid = True
    for i in range(1, len(spl)):
        page = int(spl[i])
        pages_before_curr_page = spl[:i]
        violations = np.in1d(spl[:i], rules[page])
        violation = np.any(np.in1d(spl[:i], rules[page]))
        if violation:
            line_valid = False
            break
    if line_valid:
        ex1_res += spl[int((len(spl)-1)/2)]

t1_stop = perf_counter()
print('Part A - Answer: ' + str(ex1_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(int(ex1_res), part='a', day=5, year=2024)



