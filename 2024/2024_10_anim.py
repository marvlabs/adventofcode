#!python3
'''AoC 2024 Day 10'''
from grid import Grid, step
import anim
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
     
        'name'  : 'test',
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
a = anim.AnimGrid(anim.Screen(800, 800, 'Hill Climb'), 40, 40, use_chars=True, status_area=40,\
        title='Hoof It: Climb that Mountain')#, movie = "AOC_2024-10_Hoof-it")
anim.COLORS.update(anim.make_color_gradient('gb', 'GREEN', 'BLUE', 10))
a.color_map = { ' ': 'DARK_GRAY', 'default': 'BROWN', '0': 'gb_0', '1': 'gb_1', '2': 'gb_2', '3': 'gb_3', '4': 'gb_4', '5': 'gb_5', '6': 'gb_6', '7': 'gb_7', '8': 'gb_8', '9': 'gb_9' }
ganim = Grid(40, 40, ' ')


def climb(g, pos, peaks) :
    my_height = int(g.get(pos))
    reached = False
    if my_height == 9 : 
        peaks[pos] = peaks.setdefault(pos, 0) + 1
        ganim.set(pos, str(my_height))
        a.draw(ganim, 1)
        return True

    for dir, height in g.neighbours90(pos).items() :
        if height and (int(height) == my_height+1) :
            ret = climb(g, step(pos, dir), peaks)
            reached = ret or reached
    if reached :
        ganim.set(pos, str(my_height))
        #a.draw(ganim, 1)

    return reached


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = 0
    g = Grid.from_string(aoc_input)

    for pos in g.all_pos() :
        if g.at_is(pos, '0') or g.at_is(pos, '9'):
            ganim.set(pos, g.get(pos))
    a.draw(ganim, 1000)

    for pos in g.all_pos() :
        if g.at_is(pos, '0') :
            peaks = {}
            climb(g, pos, peaks)
            p1_result += len(peaks)
            p2_result += sum(peaks.values())
    
    a.draw(ganim, 1000)
    a.save_movie()
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    #aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
