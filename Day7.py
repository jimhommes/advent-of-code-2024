from aocd import *
from time import perf_counter


def concat_num(num1, num2):
    return int(str(num1) + str(num2))


def rec_evaluate_ex1(res, curr_value, nmbr_lst):
    if len(nmbr_lst) == 1:
        if res == curr_value + nmbr_lst[0]:
            return True
        else:
            return res == curr_value * nmbr_lst[0]
    else:
        if rec_evaluate_ex1(res, curr_value + nmbr_lst[0], nmbr_lst[1:]):
            return True
        else:
            return rec_evaluate_ex1(res, curr_value * nmbr_lst[0], nmbr_lst[1:])


def rec_evaluate_ex2(res, curr_value, nmbr_lst):
    if len(nmbr_lst) == 1:
        if res == curr_value + nmbr_lst[0]:
            return True
        elif res == curr_value * nmbr_lst[0]:
            return True
        else:
            return res == concat_num(curr_value, nmbr_lst[0])
    else:
        if rec_evaluate_ex2(res, curr_value + nmbr_lst[0], nmbr_lst[1:]):
            return True
        elif rec_evaluate_ex2(res, curr_value * nmbr_lst[0], nmbr_lst[1:]):
            return True
        else:
            return rec_evaluate_ex2(res, concat_num(curr_value, nmbr_lst[0]), nmbr_lst[1:])


data_input = get_data(day=7, year=2024)
# data_input = '190: 10 19\n3267: 81 40 27\n83: 17 5\n156: 15 6\n7290: 6 8 6 15\n161011: 16 10 13\n192: 17 8 14\n21037: 9 7 18 13\n292: 11 6 16 20'

ex1_res = 0
t1_start = perf_counter()
for line in data_input.split('\n'):
    evaluate_res = int(line.split(': ')[0])
    numbers = list(map(int, line.split(': ')[1].split(' ')))
    if rec_evaluate_ex1(evaluate_res, numbers[0], numbers[1:]):
        ex1_res += evaluate_res
t1_stop = perf_counter()

print('Part A - Answer: ' + str(ex1_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(int(ex1_res), part='a', day=7, year=2024)

ex2_res = 0
t2_start = perf_counter()
for line in data_input.split('\n'):
    evaluate_res = int(line.split(': ')[0])
    numbers = list(map(int, line.split(': ')[1].split(' ')))
    if rec_evaluate_ex2(evaluate_res, numbers[0], numbers[1:]):
        ex2_res += evaluate_res
t2_stop = perf_counter()

print('Part B - Answer: ' + str(ex2_res) + ', calculated in ' + str((t2_stop - t2_start) * 1000) + ' ms')
submit(int(ex2_res), part='b', day=7, year=2024)
