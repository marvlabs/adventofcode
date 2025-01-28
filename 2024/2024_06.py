#!python3
'''AoC 2024 Day 06'''
# from pprint import pprint as pp
import re
from grid import Grid, step

#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '06',
    'url'           :   'https://adventofcode.com/2024/day/06',
    'name'          :   "Guard Gallivant: let'em walk",
    'difficulty'    :   'D2',
    'learned'       :   'grid class, once more',
    't_used'        :   '40',
    'result_p1'     :   4647,
    'result_p2'     :   1723,
}
#############
TESTS = [
    {
        'name'  : 'Guard 1',
        'input' : '''
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
''',
        'p1' : 41,
        'p2' : 6,
    },
]
#################
Headings = {
    'v' : 'S',
    '^' : 'N',
    '>' : 'E',
    '<' : 'W',
}
Turns = {
    'N' : 'E',
    'E' : 'S',
    'S' : 'W',
    'W' : 'N',
}

def find_guard(g) :
    for pos in g.all_pos() :
        if g.at_is(pos, '#') : continue
        if g.at_is(pos, '.') : continue
        return pos, Headings[g.get(pos)]


# Let the guard walk the grid.
# Return -1 if he's in a loop (for part 2)
def guard_walk(g, pos, dir) :
    steps = 0
    been_here = {} # Store all positions we've gone through with the direction
    pos_dir = lambda : pos+(dir,) # Tuple as key is faster than creating string keys like : f'{pos[0]}{pos[1]}{dir}'
    
    while g.valid(pos) :
        g.set(pos, 'X')
        been_here[pos_dir()] = True
        next_pos = step(pos, dir)
        if not g.valid(next_pos) :
            #print (f'guard_walk: out of bounds at {pos}, {dir} after {steps}')
            return steps
        if g.at_is(next_pos, '#') : 
            dir = Turns[dir]
            continue

        pos = next_pos
        steps += 1
        if pos_dir() in been_here :
            #print (f'guard_walk: been-here-before loop at {pos}, {dir} after {steps}, saving {max_steps-steps} steps')
            return - 1
        # First used brute force cycle detection: just walk for max steps. Equally fast, but not very pretty
        #if steps > max_steps :
            #print (f'guard_walk: loop after {steps}')
        #    return -1


# Try placing an obstacle in every position on the guard path to see if it creates a loop
def place_obstacle_in_path(g, path, pos, dir) :
    obstacle_positions = []
    for o_pos in path :
        gx = g.copy()
        gx.set(o_pos, '#')
        if guard_walk(gx, pos, dir) == -1 :
            obstacle_positions.append(o_pos)
    return len(obstacle_positions)


def solve(aoc_input, part1=True, part2=True, attr=None) :
    g = Grid.from_string(aoc_input)
    guard_pos, guard_dir = find_guard(g)
    
    # Part one: let the guard walk out of the grid: visited positions are X'ed
    g1 = Grid.copy(g)
    steps_taken = guard_walk(g1, guard_pos, guard_dir)
    p1_result = sum(1 for pos in g1.all_pos() if g1.get(pos) == 'X')
    #print('\n', g1, steps_taken, p1_result)

    # Part two: all positions on the path walked by the guard are candidates for an obstacle
    path = [ pos for pos in g1.all_pos() if g1.get(pos) == 'X' ]
    path.remove(guard_pos) # ...because he would notice us dropping an obstacle on him... :)
    p2_result = place_obstacle_in_path(g, path, guard_pos, guard_dir)

    return p1_result, p2_result


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
