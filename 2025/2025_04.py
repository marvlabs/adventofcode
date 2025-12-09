#!python3
'''AoC 2025 Day 04'''
from grid import Grid

#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '04',
    'url'           :   'https://adventofcode.com/2025/day/04',
    'name'          :   "Day 4: Printing Department - remove paper rolls",
    'difficulty'    :   'D2',
    'learned'       :   'Which char to compare again???',
    't_used'        :   '25',
    'result_p1'     :   1489,
    'result_p2'     :   8890,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.''',
        'p1' : 13,
        'p2' : 43,
    },
]
#################
def find_movables(g) :
    return [ pos for pos in g.all_pos() if g.at_is(pos, '@') and (sum(1 for c in g.neighbours(pos).values() if c == '@')) < 4 ]

def solve(aoc_input, part1=True, part2=True, attr=None) :
    g = Grid.from_string(aoc_input)
    movables = find_movables(g)
    p1_result = len(movables)

    p2_result = p1_result
    while len(movables) > 0 :
        for pos in movables :
            g.set(pos, 'x')
        movables = find_movables(g)
        p2_result += len(movables)
    
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
