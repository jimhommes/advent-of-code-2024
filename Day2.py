from aocd import *
import re

data_input = get_data(day=2, year=2024)
#data_input = '7 6 4 2 1\n1 2 7 8 9\n9 7 6 2 1\n1 3 2 4 5\n8 6 4 4 1\n1 3 6 7 9'
safe = []
safe_dampened = []


def validate(lst, min_diff, max_diff, dampener):
    print('Validating ' + str(lst))
    asc = lst[1] > lst[0]
    for i in range(len(lst) - 1):
        diff = lst[i+1] - lst[i]
        if asc ^ (diff > 0) or min_diff > abs(diff) or abs(diff) > max_diff:
            if dampener == 0:
                print('Returning False')
                return False
            else:
                print('Dampener is ' + str(dampener))
                return validate(lst[:i] + lst[i+1:], min_diff, max_diff, dampener - 1) or \
                       validate(lst[:i+1] + lst[i+2:], min_diff, max_diff, dampener - 1)

    print('Returning True')
    return True


for line in data_input.split('\n'):
    numbers = list(map(int, re.findall(r'\d+', line)))
    # safe.append(validate(numbers, asc=numbers[1] > numbers[0], min_diff=1, max_diff=3, dampener=0))
    safe_dampened.append(validate(numbers, min_diff=1, max_diff=3, dampener=1))

ex1_res = sum(safe)
print(ex1_res)
# submit(ex1_res, part='a', day=2, year=2024)

ex2_res = sum(safe_dampened)
print(ex2_res)
# submit(ex2_res, part='b', day=2, year=2024)