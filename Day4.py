from aocd import *
import numpy as np

lines = get_data(day=4, year=2024).split('\n')
# lines = 'MMMSXXMASM\nMSAMXMSMSA\nAMXSXMAAMM\nMSAMASMSMX\nXMASAMXAMM\nXXAMMXXAMA\nSMSMSASXSS\nSAXAMASAAA\nMAMMMXMMMM\nMXMXAXMASX'.split('\n')


def get_word_in_dir(inp, ln, x_dir, y_dir, row, col):
    if -1 <= row + ln * y_dir <= len(inp) and -1 <= col + ln * x_dir <= len(inp[0]):
        res = ''
        for i in range(ln):
            res += inp[row + i * y_dir][col + i * x_dir]
        return res
    else:
        return None


def get_words_in_all_dirs(inp, ln, row, col):
    res = []
    for (x_dir, y_dir) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            found_word = get_word_in_dir(inp, ln, x_dir, y_dir, row, col)
            if found_word is not None:
                res.append(found_word)
    return res


def get_words_x(inp, ln, row, col):
    ln_in_dir = int((ln - 1) / 2)
    return [''.join([inp[row + x][col + x] for x in range(-1 * ln_in_dir, ln_in_dir + 1)]),
            ''.join([inp[row - x][col + x] for x in range(-1 * ln_in_dir, ln_in_dir + 1)])]


def count_words(inp, word):
    cnt = 0
    for row in range(len(inp)):
        for col in range(len(inp[row])):
            if inp[row][col] == word[0]:
                # print(get_words_in_all_dirs(inp, len(word), row, col))
                cnt += sum([x == word for x in get_words_in_all_dirs(inp, len(word), row, col)])
    return cnt


def count_x_words(inp, word):
    cnt = 0
    if len(word) % 2 != 0:
        for row in range(1, len(inp) - 1):
            for col in range(1, len(inp[row]) - 1):
                if inp[row][col] == word[int((len(word)-1)/2)]:
                    wrds_x = np.array(get_words_x(inp, len(word), row, col))
                    cnt += np.all(np.logical_or(wrds_x == word, wrds_x == word[::-1]))
        return int(cnt)
    else:
        print('Error: Length of word is not odd. You can\'t make X words with these.')
        return 0

ex1_res = count_words(lines, 'XMAS')
# print(ex1_res)
# submit(ex1_res, part='a', day=4, year=2024)

ex2_res = count_x_words(lines, 'MAS')
print(ex2_res)
submit(ex2_res, part='b', day=4, year=2024)
