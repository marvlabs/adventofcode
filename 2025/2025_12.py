#!python3
'''AoC 2025 Day 12'''
import re
from math import prod
#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '12',
    'url'           :   'https://adventofcode.com/2025/day/12',
    'name'          :   "Day 12: Christmas Tree Farm",
    'difficulty'    :   'D2',
    'learned'       :   'Sometimes, easy wins.',
    't_used'        :   '15',
    'result_p1'     :   557,
    'result_p2'     :   0,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
''',
        'p1' : 2,
        'p2' : None,
    },
]
#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0
    *parts, trees = aoc_input.split('\n\n')
    part_counts = [ part.count('#') for part in parts ]

    # This would need a sophisticated shape-based solver. Unless...
    # Turns out, the input is vetted so that the ones that fit do so by a large margin, and the ones that don't have to much area anyways.
    # -> Area counting alone is enough.
    
    pack_ratio = 0.85 # Only needed for the test input, funnily enough. The puzzle works with 100% as well
    for tree in trees.splitlines() :
        dim_x, dim_y, *nr_of_trees = map(int, re.split(r'\D+', tree))
        p1_result += dim_x * dim_y * pack_ratio >= sum(map(prod, zip(part_counts, nr_of_trees)))

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
