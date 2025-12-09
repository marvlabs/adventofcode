#!python3
'''AoC 2025 Day 03'''
# from pprint import pprint as pp
import re
#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '03',
    'url'           :   'https://adventofcode.com/2025/day/03',
    'name'          :   "Day 3: Lobby - find joltage maxen",
    'difficulty'    :   'D1',
    'learned'       :   'pos <> pos-1',
    't_used'        :   '20',
    'result_p1'     :   17113,
    'result_p2'     :   169709990062889,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''987654321111111
811111111111119
234234234234278
818181911112111''',
        'p1' : 357,
        'p2' : 3121910778619,
    },
]
#################

def joltage_1(batteries) :
    numbers = list(map(int, list(batteries)))
    d1 = max(numbers[0:-1])
    d1_pos = numbers.index(d1)
    d2 = max(numbers[d1_pos+1:])
    return 10*d1 + d2


def joltage_2(batteries, nr) :
    joltage = 0
    pos = 0
    end = len(batteries)
    numbers = list(map(int, list(batteries)))
    for i in range(nr, 0, -1) :
        di = max(numbers[pos:end-i+1])
        di_pos = numbers[pos:].index(di)
        pos = pos+di_pos+1
        joltage = 10 * joltage + di
    return joltage


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0
    for string in aoc_input.splitlines()  :
        if string == '' : continue
        p1_result += joltage_1(string)
        p2_result += joltage_2(string, 12)
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
