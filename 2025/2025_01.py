#!python3
'''AoC 2025 Day 01'''
# from pprint import pprint as pp
import re
#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '01',
    'url'           :   'https://adventofcode.com/2025/day/01',
    'name'          :   "Day 1: Secret Entrance - turn that dial",
    'difficulty'    :   'D1',
    'learned'       :   '...so many special cases to err on...',
    't_used'        :   '30',
    'result_p1'     :   1165,
    'result_p2'     :   6496,
}
#############
TESTS = [
 {
        'name'  : 'dial-1',
        'input' : '''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
''',
        'p1' : 3,
        'p2' : 6,
    },
]
#################
def turn_1(pos, instructions):
    zeros = 0
    for instruction in instructions :
        pos = (pos + int(instruction[1:]) * (-1 if instruction[0] == 'L' else 1)) % 100
        if pos == 0 : zeros += 1
    return zeros

def turn_2(pos, instructions):
    zeros = 0
    for instruction in instructions :
        clicks = int(instruction[1:])
        dir = instruction[0]
        if pos != 0 and ((dir == 'L' and clicks%100 > pos) or (dir == 'R' and clicks%100 > (100 - pos))) :
            zeros += 1 # crossing zero with even without the 100s
        if clicks >= 100 :
            zeros += clicks // 100 - (1 if pos == 0 and clicks % 100 == 0 else 0) # crossing zeros multiple times, but correct if on 0 and back on zero
        pos = (pos + clicks * (-1 if dir == 'L' else 1)) % 100
        if pos == 0 : zeros += 1
    return zeros


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = turn_1(50, aoc_input.splitlines())
    p2_result = turn_2(50, aoc_input.splitlines())
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
