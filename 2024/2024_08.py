#!python3
'''AoC 2024 Day 08'''
# from pprint import pprint as pp
import re
from grid import Grid, step

#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '08',
    'url'           :   'https://adventofcode.com/2024/day/08',
    'name'          :   "Resonant Collinearity: Antennas and Antinodes",
    'difficulty'    :   'D2',
    'learned'       :   'lambda functions',
    't_used'        :   '35',
    'result_p1'     :   320,
    'result_p2'     :   1157,
}
#############
TESTS = [
 {
        'name'  : 'T-Map',
        'input' : '''
T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........
''',
        'p1' : None,
        'p2' : 9,
    },
 {
        'name'  : 'A0-Map',
        'input' : '''
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
''',
        'p1' : 14,
        'p2' : 34,
    },]
#################
def scan_map(g) :
    antennas = {}
    for pos in g.all_pos() :    
        if g.at_is(pos, '.') : continue
        antennas.setdefault(g.get(pos), []).append(pos)
    return antennas

posdiff = lambda p1, p2 : (p1[0]-p2[0], p1[1]-p2[1])
posadd  = lambda p1, p2 : (p1[0]+p2[0], p1[1]+p2[1])

def create_antinodes(antennas, g, infinite = False) :
    antinodes = {}
    for ant in antennas :
        for pos1 in antennas[ant] :
            for pos2 in antennas[ant] :
                if pos1 == pos2 : continue
                if infinite : # Add the antenna positions themselves as antinodes in part 2
                    antinodes[pos1] = True
                    antinodes[pos2] = True

                diff = posdiff(pos2, pos1)
                pos_antinode = posadd(pos2, diff)
                while g.valid(pos_antinode) :
                    #print("creating antinode", pos1, pos2, posdiff(pos2, pos1) , pos_antinode)
                    antinodes[pos_antinode] = True
                    if not infinite: break
                    pos_antinode = posadd(pos_antinode, diff)

    return antinodes


def solve(aoc_input, part1=True, part2=True, attr=None) :
    g = Grid.from_string(aoc_input)
    antennas = scan_map(g)
    antinodes_1 = create_antinodes(antennas, g, infinite=False)
    antinodes_2 = create_antinodes(antennas, g, infinite=True)

    return len(antinodes_1), len(antinodes_2)

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
