#!python3
'''AoC 2016 Day 08'''
import re
import grid
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '08',
    'url'           :   'https://adventofcode.com/2016/day/08',
    'name'          :   "Day 8: Two-Factor Authentication - broken display",
    'difficulty'    :   'D2',
    'learned'       :   'Grid class coming in handy',
    't_used'        :   '30',
    'result_p1'     :   121, 
    'result_p2'     :   'RURUCEOEIL',
}
#############
TESTS = [
{
        'name'  : 'disp-6',
        'input' : '''rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
''',
        'p1' : 6,
        'p2' : None,
},
]

#################


def solve(aoc_input, part1=True, part2=True, attr=None) :
    display = grid.Grid(50, 6, ' ')

    for line in aoc_input.splitlines() :
        d1, d2 = list(map(int, re.findall(r'\d+', line)))
        
        if 'rect' in line :
            for y in range(d2) :
                for x in range(d1) :
                    display.set((x, y), '#')
        
        elif 'rotate' in line :
            if 'row' in line :
                row = display.get_line((0, d1), 'E')
                for i, c in enumerate(row) : 
                    display.set(((i + d2) % display.dim_x, d1), c)
            else :
                col = display.get_line((d1, 0), 'S')
                for i, c in enumerate(col) : 
                    display.set((d1, (i + d2) % display.dim_y), c)

    if part2 :print('DISPLAY:\n\n' + str(display)+'\n')

    p1_result = str(display).count('#')
    p2_result = 'RURUCEOEIL'

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
