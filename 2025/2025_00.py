#!python3
'''AoC 2025 Day xx'''
import re
#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   'xx',
    'url'           :   'https://adventofcode.com/2025/day/xx',
    'name'          :   "title",
    'difficulty'    :   'D',
    'learned'       :   '',
    't_used'        :   '0',
    'result_p1'     :   0,
    'result_p2'     :   0,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''
testlines
here
''',
        'p1' : 42,
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
