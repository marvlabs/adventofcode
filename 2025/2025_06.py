#!python3
'''AoC 2025 Day 06'''
import re
from math import prod
#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '06',
    'url'           :   'https://adventofcode.com/2025/day/06',
    'name'          :   "Day 6: Trash Compactor - cephalopod maths",
    'difficulty'    :   'D2',
    'learned'       :   'zipit - comprehendit',
    't_used'        :   '30',
    'result_p1'     :   6957525317641,
    'result_p2'     :   13215665360076,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
''',
        'p1' : 4277556,
        'p2' : 3263827,
    },
]
#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    lines = [ re.split(r'\s+', line.strip()) for line in aoc_input.splitlines() if line.strip() != '' ]
    p1_result = sum( sum(map(int, col[:-1])) if col[-1] == '+' else prod(map(int, col[:-1])) for col in zip(*lines) )

    # Transpose characters, put together as lines again, split into tasks
    chars = [ list(line) for line in aoc_input.splitlines() if line.strip() != '' ]
    tasks = [ t.splitlines() for t in re.split(r'\n\s*\n', '\n'.join([ ''.join(col) for col in zip(*chars) ])) ]
    p2_result = sum ( sum(int(op[:-1]) for op in task ) if task[0][-1] == '+' else prod(int(op[:-1]) for op in task ) for task in tasks )

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
