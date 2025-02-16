#!python3
'''AoC 2016 Day 22'''
import re
from itertools import permutations
from grid import Grid, step
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '22',
    'url'           :   'https://adventofcode.com/2016/day/22',
    'name'          :   "Grid Computing - move data around",
    'difficulty'    :   'D2',
    'learned'       :   'Closely check the problem description and input :)',
    't_used'        :   '60',
    'result_p1'     :   903, 
    'result_p2'     :   215,
}
#############
TESTS = [
{
    'name'  : '6T-data',
    'input' : '''Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   100T    80T     20T   80%
/dev/grid/node-x0-y1   110T    60T     50T   54%
/dev/grid/node-x0-y2   320T   280T     40T   87%
/dev/grid/node-x1-y0    90T    70T     20T   77%
/dev/grid/node-x1-y1    80T    00T     80T    0%
/dev/grid/node-x1-y2   110T    70T     40T   63%
/dev/grid/node-x2-y0   100T    60T     40T   60%
/dev/grid/node-x2-y1    90T    80T     10T   88%
/dev/grid/node-x2-y2    90T    60T     30T   66%''',
    'p1' : None,
    'p2' : 7,
},
]

#################
wall = '#'
hall = '.'

def solve(aoc_input, part1=True, part2=True, attr=None) :
    # Parse input into tuple(row, column, size, used, avail, percent)
    comps = [ tuple(map(int, re.findall(r'\d+', line))) for line in aoc_input.splitlines() if line.startswith('/dev') ]
    p1_result = sum( [ c1[3] <= c2[4] for c1, c2 in permutations(comps, 2) if c1[3] > 0 ] )

    # Checking the layout of the computer grid from the puzzle input:
    grid = Grid(max(c[0] for c in comps)+1, max(c[1] for c in comps)+1)
    pos_empty = None
    pos_data = (grid.dim_x-1, 0)
    for c in comps :
        pos = (c[0], c[1])
        used = c[3]
        sign = hall
        if used > 90 : 
            sign = wall
        elif used == 0:
            pos_empty = pos
        grid.set(pos, sign)
    grid.set(pos_empty, '-')
    grid.set(pos_data, 'G')

    # print()
    # print(grid)
    # ... looks equivalent to the example: some whales (don't touch) and an empty one. The rest should all be shiftable
    # - Data G needs to travel left dim_x - 1 from (dim_x - 1, 0 ) to (0,0)
    # - The empty space _ needs to travel from its position to one left of data G
    # - How much moving does the free space _ need to do... : 
    #   - shortest path to one field left of G:
    #     up its y. left/right around all the whale's (####) and to dim-x-2, one pos left of data G 
    #     --> use the flood fill alg from day 13 to compute it (I manually counted 34)
    move_to_data = flood_it(grid, pos_empty, step(pos_data, 'W'))
    # To move the data G left, we need to:
    # - move data left to the empty space we just created => one move
    # - repeat these next 5 moves, times dim_x-2
    #   - move the free space down / left / left / up
    #   - move data left
    p2_result = move_to_data + 1 + 5*(grid.dim_x-2)

    return p1_result, p2_result


# Flood fill search: fill the maze step by step until we hit the end position
def flood_it(maze, start, end) :
    nr_of_steps = -1 # because we also do a step to reach the start
    to_visit = [start]
    seen = set()

    while True :
        nr_of_steps += 1
        next_positions = set()

        while len(to_visit) :
            pos = to_visit.pop()
            seen.add(pos)
            if pos == end : 
                return nr_of_steps

            for _, neighbour_pos, tile in maze.valid_neighbours90(pos) :
                if neighbour_pos not in seen and tile == hall :
                    next_positions.add(neighbour_pos)

        to_visit = next_positions

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
