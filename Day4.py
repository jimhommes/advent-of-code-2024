from aocd import *

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


def count_words(inp, word):
    cnt = 0
    for row in range(len(inp)):
        for col in range(len(inp[row])):
            if inp[row][col] == word[0]:
                # print(get_words_in_all_dirs(inp, len(word), row, col))
                cnt += sum([x == word for x in get_words_in_all_dirs(inp, len(word), row, col)])
    return cnt


ex1_res = count_words(lines, 'XMAS')
print(ex1_res)
submit(ex1_res, part='a', day=4, year=2024)
