#!python3
'''AoC 2024 Day 15'''
# from pprint import pprint as pp
import re
from grid import Grid, step

#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '15',
    'url'           :   'https://adventofcode.com/2024/day/15',
    'name'          :   "Warehouse Woes: why don't these crates rotate???",
    'difficulty'    :   'D2',
    'learned'       :   'nice exercise',
    't_used'        :   '45',
    'result_p1'     :   1509863,
    'result_p2'     :   1548815,
}
#############
TESTS = [
{
'name'  : 'Warehouse-small',
'input' : '''
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<''',
'p1' : 2028,
'p2' : None,
},

{
'name'  : 'Warehouse-small-2',
'input' : '''
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^''',
'p1' : None,
'p2' : 618,
},

{
    'name'  : 'Warehouse-mid',
    'input' : '''
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^''',
    'p1' : 10092,
    'p2' : 9021,
},
]

#################


def solve(aoc_input, part1=True, part2=True, attr=None) :
    layout, instructions = aoc_input.split( "\n\n" )
    wh_1 = Grid.from_string(layout)
    wh_2, robo_pos_1, robo_pos_2 = double(wh_1)
    directions = [ {'<':'W', '>':'E', '^':'N', 'v':'S'}[d] for d in list(instructions) if d in '<>^v' ]

    for dir in directions :
        robo_pos_1 = try_move(wh_1, robo_pos_1, dir) or robo_pos_1
    p1_result = sum(pos[0]+100*pos[1] for pos in wh_1.all_pos() if wh_1.at_is(pos, 'O'))

    for dir in directions :
        if dir in ['E', 'W'] :
            robo_pos_2 = try_move(wh_2, robo_pos_2, dir) or robo_pos_2
        if dir in ['S', 'N'] :
            if can_move_wide(wh_2, robo_pos_2, dir) :
                robo_pos_2 = do_move_wide(wh_2, robo_pos_2, dir)
    p2_result = sum(pos[0]+100*pos[1] for pos in wh_2.all_pos() if wh_2.at_is(pos, '['))

    return p1_result, p2_result


def can_move_wide(wh, pos, dir) :
    new_pos = step(pos, dir)

    if wh.at_is(new_pos, '.') :
        return True

    if wh.at_is(new_pos, '[') :
        return can_move_wide(wh, new_pos, dir) and can_move_wide(wh, step(new_pos, 'E'), dir)

    if wh.at_is(new_pos, ']') :
        return can_move_wide(wh, new_pos, dir) and can_move_wide(wh, step(new_pos, 'W'), dir)

    return False


def do_move_wide(wh, pos, dir) :
    new_pos = step(pos, dir)

    if wh.at_is(new_pos, '[') :
        do_move_wide(wh, new_pos, dir)
        do_move_wide(wh, step(new_pos, 'E'), dir)

    if wh.at_is(new_pos, ']') :
        do_move_wide(wh, new_pos, dir)
        do_move_wide(wh, step(new_pos, 'W'), dir)

    wh.set(new_pos, wh.get(pos))
    wh.set(pos, '.')
    return new_pos


def try_move(wh, pos, dir) :
    new_pos = step(pos, dir)

    if wh.get(new_pos) in 'O[]':
        try_move(wh, new_pos, dir)

    if wh.at_is(new_pos, '.') :
        wh.set(new_pos, wh.get(pos))
        wh.set(pos, '.')
        return new_pos

    return None

def double(wh) :
    wh2 = Grid(wh.dim_x*2, wh.dim_y)
    for pos in wh.all_pos() :
        c = wh.get(pos)
        if c == '@' : 
            robo_pos = pos
            robo_pos_2 = (pos[0]*2, pos[1])

        wh2.set((pos[0]*2, pos[1]), c if c != 'O' else '[')
        wh2.set((pos[0]*2+1, pos[1]), {'.' : '.', '#' : '#', 'O': ']', '@': '.'}[c])
    
    return wh2, robo_pos, robo_pos_2

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
