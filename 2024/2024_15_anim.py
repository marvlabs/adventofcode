#!python3
'''AoC 2024 Day 15'''
from grid import Grid, step
import anim
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

a = anim.AnimGrid(anim.Screen(1200, 650, 'Shift them Crates!'), 100, 50, 
    use_chars=False, status_area=50, 
    title='AOC 2024-15 Warehouse Woes - Random Rampaging Robot',
)#movie = "AOC_2024-15_Warehouse-Woes")
a.color_map = { '.': 'BLACK', '#': 'ORANGE', '0': 'TEAL', '[': 'TEAL', ']': 'TEAL', '@': 'RED', 'default': 'PINK' }

def solve(aoc_input, part1=True, part2=True, attr=None) :
    layout, instructions = aoc_input.split( "\n\n" )
    wh_1 = Grid.from_string(layout)
    wh_2, robo_pos_1, robo_pos_2 = double(wh_1)
    directions = [ {'<':'W', '>':'E', '^':'N', 'v':'S'}[d] for d in list(instructions) if d in '<>^v' ]

    for dir in directions :
        robo_pos_1 = try_move(wh_1, robo_pos_1, dir) or robo_pos_1
    p1_result = sum(pos[0]+100*pos[1] for pos in wh_1.all_pos() if wh_1.at_is(pos, 'O'))


    a.draw(wh_2, 1000, f'({robo_pos_2[0]:3}, {robo_pos_2[1]:3})')
    for i, dir in enumerate(directions) :
        if (i < 300 or (i>3000 and i < 3600) or i > 19400) \
            and i % 5 == 0 : a.draw(wh_2, 30, f'Instruction: {i:5d} ({robo_pos_2[0]:3}, {robo_pos_2[1]:3})')

        if dir in ['E', 'W'] :
            robo_pos_2 = try_move(wh_2, robo_pos_2, dir) or robo_pos_2
        if dir in ['S', 'N'] :
            if can_move_wide(wh_2, robo_pos_2, dir) :
                robo_pos_2 = do_move_wide(wh_2, robo_pos_2, dir)
    p2_result = sum(pos[0]+100*pos[1] for pos in wh_2.all_pos() if wh_2.at_is(pos, '['))
    
    a.draw(wh_2, 2000, f'P1: {p1_result}, P2: {p2_result}')
    a.save_movie()

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

    if wh.at_is(new_pos, '.') :
        wh.set(new_pos, wh.get(pos))
        wh.set(pos, '.')
        return new_pos

    if wh.get(new_pos) in 'O[]':
        if try_move(wh, new_pos, dir) :
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
    #aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
