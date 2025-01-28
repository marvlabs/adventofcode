#!python3
'''AoC 2024 Day 25'''
from grid import Grid, step
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '25',
    'url'           :   'https://adventofcode.com/2024/day/25',
    'name'          :   "Code Chronicle",
    'difficulty'    :   'D1',
    'learned'       :   'Sometimes it just works :-)',
    't_used'        :   '10',
    'result_p1'     :   2815,
    'result_p2'     :   0,
}
#############
TESTS = [
 {
        'name'  : 'some-keys',
        'input' : '''
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
''',
        'p1' : 3,
        'p2' : None,
    },
]
#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0

    locks = []
    keys = []

    for pattern in aoc_input.split('\n\n') :
        lock, key = get_pattern_id(Grid.from_string(pattern))
        if lock : locks.append(lock)
        if key  : keys.append(key)

    p1_result = sum( [ 1 for key in keys for lock in locks if fits(key, lock) ] )

    return p1_result, p2_result


def fits(key, lock) :
    for i in range(5) :
        if key[i] + lock[i] > 5 :
            return False
    return True


def get_pattern_id(pattern) :
    id = [-1,-1,-1,-1,-1]

    for x in range(pattern.dim_x) :
        for y in range(pattern.dim_y) :
            id[x] += 1 if pattern.get((x,y)) == '#' else 0
    
    if pattern.at_is((0,0), '#') :
        return id, None
    else :
        return None, id


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
