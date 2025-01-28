#!python3
'''AoC 2024 Day 07'''
# from pprint import pprint as pp
import re
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '07',
    'url'           :   'https://adventofcode.com/2024/day/07',
    'name'          :   "Bridge Repair: lots of equations possible",
    'difficulty'    :   'D2',
    'learned'       :   'BE CAREFUL when recursing... REVERSED!',
    't_used'        :   '60',
    'result_p1'     :   20281182715321,
    'result_p2'     :   159490400628354,
}
#############
TESTS = [
 {
        'name'  : 'Easy Equations',
        'input' : \
'''156: 15 6
190: 10 19
3267: 81 40 27
83: 17 5
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20''',
        'p1' : 3749,
        'p2' : 11387,
    },
]
#################
calls = 0
def visited() :
    global calls
    calls += 1

# Forward version...
def find_working_equation(desired, result_so_far, numbers_left, concat) :
    #visited()
    if len(numbers_left) == 0 :
        return result_so_far if result_so_far == desired else 0
    if result_so_far > desired :
        return 0

    return (concat and \
           find_working_equation(desired, int(str(result_so_far) + str(numbers_left[0])), numbers_left[1:], concat)) \
        or find_working_equation(desired, result_so_far + numbers_left[0], numbers_left[1:], concat) \
        or find_working_equation(desired, result_so_far * numbers_left[0], numbers_left[1:], concat)


# BACKWARDS! What an idea someone had :)
# The above can be greatly optimzed by working backward from the result through the number list.
# Take the desired result and apply the opposite operators in reverse order (minus, div, unconcat)
# A lot of paths don't need to be tried:
# - can't be a multiply if the division leaves a rest
# - can't be a concat if the numbers don't match the end of the result
# - can't be an addition if the subtraction is negative
# -> speed up is more than 100x

# Needs an undo of the possible concatenation: 1234, 34 -> 12 and 123, 4 -> 0
def unconcat(result_so_far, prev_number):
    str_result = str(result_so_far)
    str_next_nr = str(prev_number)
    if str_result.endswith(str_next_nr) and len(str_result) > len(str_next_nr) :
        return int(str_result[:-len(str_next_nr)])
    return 0

def find_working_equation_backwards(desired, result_so_far, numbers_left, concat) :
    #visited()
    if len(numbers_left) == 0 :
        return True if result_so_far == desired else 0

    prev_number = numbers_left[-1]

    return (concat and (split_result := unconcat(result_so_far, prev_number)) and \
            find_working_equation_backwards(desired, split_result, numbers_left[:-1], concat)) \
        or ((result_so_far - prev_number >= 0) and find_working_equation_backwards(desired, result_so_far - prev_number, numbers_left[:-1], concat)) \
        or ((result_so_far % prev_number == 0) and find_working_equation_backwards(desired, result_so_far // prev_number, numbers_left[:-1], concat))


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0
    for string in aoc_input.splitlines()  :
        desired, numberstr = re.match(r'(.*): (.*)', string).groups()
        numbers = list(map(int, numberstr.split()))
        #p1_result += find_working_equation(int(desired), numbers[0], numbers[1:], concat=False)
        #p2_result += find_working_equation(int(desired), numbers[0], numbers[1:], concat=True)
        p1_result += int(desired) if find_working_equation_backwards(numbers[0], int(desired), numbers[1:], concat=False) else 0
        p2_result += int(desired) if find_working_equation_backwards(numbers[0], int(desired), numbers[1:], concat=True) else 0
    #print(f'Recursion visited {calls} times')
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
