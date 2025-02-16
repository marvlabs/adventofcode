#!python3
'''AoC 2016 Day 12'''
from assembunny import Assembunny
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '12',
    'url'           :   'https://adventofcode.com/2015/day/12',
    'name'          :   "Leonardo's Monorail - Assembunny code",
    'difficulty'    :   'D2',
    'learned'       :   'Tweaked the simulator from 2015-23',
    't_used'        :   '15',
    'result_p1'     :   318083,
    'result_p2'     :   9227737,
}
#############
TESTS = [
{
        'name'  : 'small prog',
        'input' : '''cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a''',
        'p1' : 42,
        'p2' : None,
},
]

#################
# Assembunny's first apperance. As it got re-used on days 12 and 23 it's been refactored to the assembunny.py module

def solve(aoc_input, part1=True, part2=True, attr=None) :
    results = []
    bunny = Assembunny(aoc_input, do_optimize=True)
    for input_value in (0, 1) :
        bunny.reset()
        bunny.set('c', input_value)
        bunny.run()
        results.append(bunny.get('a'))

    return results

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
