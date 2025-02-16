#!python3
'''AoC 2016 Day xx'''
import re
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   'xx',
    'url'           :   'https://adventofcode.com/2016/day/xx',
    'name'          :   "name",
    'difficulty'    :   'Dx',
    'learned'       :   '',
    't_used'        :   '0',
    'result_p1'     :   None, 
    'result_p2'     :   None,
}
#############
TESTS = [
{
    'name'  : 'sometest',
    'input' : '''To continue, please consult the code grid in the manual.  Enter the code at row 4, column 4.''',
    'p1' : None,
    'p2' : None,
},
]

#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = 0
    #row, column =  re.findall(r'\d+', aoc_input)

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
