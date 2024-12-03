from aocd import *
import numpy as np
import re

data_input = get_data(day=2, year=2024)
# data_input = '7 6 4 2 1\n1 2 7 8 9\n9 7 6 2 1\n1 3 2 4 5\n8 6 4 4 1\n1 3 6 7 9\n1 5 6 7 8 9\n1 2 3 4 8\n1 2 3 2 1\n1 2 8 4 5'
safe = []
safe_dampened = []


def validate(lst, min_diff, max_diff, dampener):
    # print('Validating ' + str(lst))
    difflst = np.diff(lst)
    asc = difflst > 0
    dec = difflst < 0

    dir_valid = asc if sum(asc) > sum(dec) else dec
    bounds_valid = np.logical_and(max_diff >= np.abs(difflst), np.abs(difflst) >= min_diff)

    valid = np.logical_and(dir_valid, bounds_valid)
    # print(valid)
    # print(sum(np.logical_not(valid)))

    if np.all(valid):
        # print('All valid, returning True')
        return True
    elif dampener > 0:
        # print('Less errors than dampeners. Amount of errors: ' + str(sum(np.logical_not(valid))) + ', dampeners: ' + str(dampener))
        for error_index in np.where(valid == 0)[0].astype(int):
            # print('Errors indices: ' + str(np.where(valid == 0)[0].astype(int)))
            nxtlst1 = np.append(lst[:error_index], lst[error_index+1:])
            # print('Partly validation for part 1: ' + str(nxtlst1))
            nxtlst2 = np.append(lst[:error_index+1], lst[error_index+2:])
            # print('Partly validation for part 2: ' + str(nxtlst2))
            return validate(nxtlst1, min_diff, max_diff, dampener - 1) or \
                   validate(nxtlst2, min_diff, max_diff, dampener - 1)
    else:
        # print('returning False')
        return False


for line in data_input.split('\n'):
    numbers = np.array(re.findall(r'\d+', line)).astype(int)
    safe.append(validate(numbers, min_diff=1, max_diff=3, dampener=0))
    safe_dampened.append(validate(numbers, min_diff=1, max_diff=3, dampener=1))

ex1_res = sum(safe)
print(ex1_res)
submit(ex1_res, part='a', day=2, year=2024)

ex2_res = sum(safe_dampened)
print(ex2_res)
submit(ex2_res, part='b', day=2, year=2024)
