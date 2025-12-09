#!python3
'''AoC 2025 Day 04'''
from grid import Grid
import anim

#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '04',
    'url'           :   'https://adventofcode.com/2025/day/04',
    'name'          :   "Day 4: Printing Department - remove paper rolls",
    'difficulty'    :   'D2',
    'learned'       :   'which char to compare???',
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
    p2_result = 0

    a = anim.AnimGrid(anim.Screen(1260,1260, 'Paper Rolls'), g.dim_x, g.dim_y, use_chars=False, status_area=50, 
        title='AOC 2025 DAY 4 - Printing Department', movie = "AOC_2025-04_Printing_Department")
    a.color_map = { '.': 'DARK_GRAY', '@': 'BLUE', 'X': 'RED', 'x': 'LIGHT_GRAY', 'default': 'BLACK' }

    a.draw(g, 1200, f'Movables: {0}   Removed: {0}')


    p2_result = p1_result
    round = 0
    while len(movables) > 0 :
        round += 1
        frame = 0
        for pos in movables :
            g.set(pos, 'X')
            frame += 1
            if frame % 50 == 0 : a.draw(g, 1, f'Round {round}   Movables: {len(movables)}   Removed: {p2_result}')
        a.draw(g, 150, f'Round {round}   Movables: {len(movables)}   Removed: {p2_result}')
        for pos in movables :
            g.set(pos, 'x')
        #a.draw(g, 10)
        movables = find_movables(g)
        p2_result += len(movables)
    
    a.draw(g, 3000, f'Round {round}   Movables: {len(movables)}   Removed: {p2_result}')
    a.save_movie(fps=30)
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    #aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
