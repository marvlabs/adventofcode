#!python3
'''AoC 2024 Day 04'''
# from pprint import pprint as pp
import re
from grid import Grid, step

#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '04',
    'url'           :   'https://adventofcode.com/2024/day/04',
    'name'          :   "Ceres Search: X marks the Grid",
    'difficulty'    :   'D2',
    'learned'       :   'my own grid class, again',
    't_used'        :   '45',
    'result_p1'     :   2507,
    'result_p2'     :   1969,
}
#############
TESTS = [
    {
        'name'  : 'XMAS 18',
        'input' : '''
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
''',
        'p1' : 18,
        'p2' : 9,
    },
    {
        'name'  : 'X-MAS 9',
        'input' : '''
.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
''',
        'p1' : 0,
        'p2' : 9,
    },
    {
        'name'  : 'X-MAS small',
        'input' : '''
..X...
.SAMX.
.A..A.
XMAS.S
.X....
''',
        'p1' : 4,
        'p2' : 0,
    },]
#################

def find_XMAS(g):
    res = 0
  
    #print("\n" + str(g))
    res += str(g).count('XMAS') + str(g).count('SAMX')

    g90 = Grid(g.dim_y, g.dim_x)
    for x in range(g.dim_x) :
        for y in range(g.dim_y) :
            g90.set((y,x), g.get((x,y)))
    #print("\n" + str(g90))
    res += str(g90).count('XMAS') + str(g90).count('SAMX')

    diagonals_NE = ''
    x = 0
    for y in range(g.dim_y) :
        diagonals_NE += g.get_line((x,y), 'NE') + '\n'
    for x in range(1,g.dim_x) :
        diagonals_NE += g.get_line((x,y), 'NE') + '\n'
    res += diagonals_NE.count('XMAS') + diagonals_NE.count('SAMX')

    diagonals_NW = ''
    for x in range(g.dim_x) :
        diagonals_NW += g.get_line((x,y), 'NW') + '\n'
    for y in range(g.dim_y-2, 0, -1) :
        diagonals_NW += g.get_line((x,y), 'NW') + '\n'
    res += diagonals_NW.count('XMAS') + diagonals_NW.count('SAMX')

    return res

def find_CROSS_MAS(g):
    res = 0
    for pos in g.all_pos() :
        if g.is_border(pos) : continue
        if g.get(pos) != 'A' : continue
    
        n = g.neighbours(pos)
        if n['NE'] + n['SW'] in ['MS', 'SM'] and n['NW'] + n['SE'] in ['MS', 'SM'] :
            res += 1

    return res
 

def solve(aoc_input, part1=True, part2=True, attr=None) :
    g = Grid.from_string(aoc_input)
    return find_XMAS(g), find_CROSS_MAS(g)


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
