#!python3
'''AoC 2015 Day xx'''
# from pprint import pprint as pp
import re
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '20',
    'url'           :   'https://adventofcode.com/2015/day/20',
    'name'          :   "Infinite Elves and Infinite Houses",
    'difficulty'    :   'D',
    'learned'       :   '',
    't_used'        :   '0',
    'result_p1'     :   0,
    'result_p2'     :   0,
}
#############
TESTS = [
 {
        'name'  : 't-9',
        'input' : '130',
        'p1' : 9,
        'p2' : None,
    },
]
#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    p1_result, p2_result = 0, 0
    for string in aoc_input.splitlines()  :
        if string == '' : continue
        v1, v2 = re.match(r'(.*) (\d+)', string).groups()
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
