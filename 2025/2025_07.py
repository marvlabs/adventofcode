#!python3
'''AoC 2025 Day 07'''
from grid import Grid, step
import functools
#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '07',
    'url'           :   'https://adventofcode.com/2025/day/07',
    'name'          :   "Day 7: Laboratories - tachyons and quantum tachyons",
    'difficulty'    :   'D2',
    'learned'       :   'WTF? No bruteforce??? Iterative beats recursion.',
    't_used'        :   '30',
    'result_p1'     :   1662,
    'result_p2'     :   40941112789504,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
''',
        'p1' : 21,
        'p2' : 40,
    },
]
#################

# Classical Tachyons
def count_splits(g, s):
    splits = 0
    beams_in_row = {s}

    for y in range(1, g.dim_y) :
        new_beams = set()
        for x in beams_in_row :
            if g.at_is((x,y), '^') :
                splits += 1
                if x>0         : new_beams.add(x-1)
                if x<g.dim_x-1 : new_beams.add(x+1)
            else:
                new_beams.add(x)
        beams_in_row = new_beams
    
    return splits


# Quantum Tachyons
def count_timelines(g, s):
    timelines = { s : 1 } # nr of timelines reaching position x in row

    for y in range(1, g.dim_y) :
        new_timelines = {}
        for x in timelines.keys() :
            if g.at_is((x,y), '^') :
                if x>0         : new_timelines[x-1] = new_timelines.get(x-1,0) + timelines[x]
                if x<g.dim_x-1 : new_timelines[x+1] = new_timelines.get(x+1,0) + timelines[x]
            else:
                new_timelines[x] = new_timelines.get(x,0) + timelines[x]
        timelines = new_timelines
    return sum(timelines.values())


# Just for the fun of it: A recursive quantum tachyon counter, memoized 😃
# It's much slower than the iterative version above, but it's fun to see it work.
@functools.cache
def be_a_quantum_tachyon(g, pos):
    if not g.valid(pos)      : return 0 # Outside
    if pos[1] == g.dim_y - 1 : return 1 # Bottom row

    if (g.at_is(step(pos, 'S'), '^')):  # Split left and right (no checks for ^^ double splitters)
        return ( be_a_quantum_tachyon(g, step(pos, 'SE'))
               + be_a_quantum_tachyon(g, step(pos, 'SW')))
    else:                               # Straight down
        return   be_a_quantum_tachyon(g, step(pos, 'S'))


def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    g = Grid.from_string(aoc_input)
    s = g.get_line( (0,0), 'E' ).index('S')

    p1_result = count_splits(g, s)
    p2_result = count_timelines(g, s)
    #p2_result = be_a_quantum_tachyon(g, (s,0))

    return p1_result, p2_result


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
