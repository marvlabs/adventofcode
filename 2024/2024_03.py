#!python3
'''AoC 2024 Day 03'''
# from pprint import pprint as pp
import re
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '03',
    'url'           :   'https://adventofcode.com/2024/day/03',
    'name'          :   "Mull It Over: find the mul()s",
    'difficulty'    :   'D1',
    'learned'       :   'REALLY check the indents in Python :D',
    't_used'        :   '30',
    'result_p1'     :   156388521,
    'result_p2'     :   75920122,
}
#############
TESTS = [
    {
        'name'  : 'Muls',
        'input' : '''
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5)
''',
        'p1' : 161,
        'p2' : None,
    },
 {
        'name'  : 'Do Muls',
        'input' : '''
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))''',
        'p1' : None,
        'p2' : 48,
    },
]
#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0

    muls = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', aoc_input)
    p1_result += sum(list(int(x)*int(y) for x,y in muls))

    dos = re.findall(r'do\(\)(.*?)don\'t\(\)', "do()" + aoc_input + "don't()", flags=re.DOTALL)
    for do in dos :
        muls = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', do)
        p2_result += sum(list(int(x)*int(y) for x,y in muls))

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
