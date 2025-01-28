#!python3
'''AoC 2024 Day 10'''
from grid import Grid, step
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '10',
    'url'           :   'https://adventofcode.com/2024/day/10',
    'name'          :   "Hoof It: Climb that Mountain",
    'difficulty'    :   'D2',
    'learned'       :   'Nice code pays off :-)',
    't_used'        :   '20',
    'result_p1'     :   461,
    'result_p2'     :   875,
}
#############
TESTS = [
    {
        'name'  : 'Small Hills',
        'input' : '''
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
''',
        'p1' : 36,
        'p2' : 81,
    },
]
#################

def climb(g, pos, peaks) :
    my_height = int(g.get(pos))
    if my_height == 9 : 
        # incrementing here paid off for part 2: just needed to sum those :-)
        peaks[pos] = peaks.setdefault(pos, 0) + 1
        return

    for dir, height in g.neighbours90(pos).items() :
        if height and (int(height) == my_height+1) :
            climb(g, step(pos, dir), peaks)
    return


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = 0
    g = Grid.from_string(aoc_input)

    for pos in g.all_pos() :
        if g.at_is(pos, '0') :
            peaks = {}
            climb(g, pos, peaks)
            p1_result += len(peaks)
            p2_result += sum(peaks.values())
    
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
