#!python3
'''AoC 2016 Day 02'''
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '02',
    'url'           :   'https://adventofcode.com/2016/day/02',
    'name'          :   "Bathroom Security - overengineered keypad",
    'difficulty'    :   'D2',
    'learned'       :   'Maps help, hexmaps doubly so',
    't_used'        :   '20',
    'result_p1'     :   '56855', 
    'result_p2'     :   'B3C27',
}
#############
TESTS = [
{
        'name'  : 'kp-5',
        'input' : '''ULL
RRDDD
LURDL
UUUUD''',
        'p1' : '1985',
        'p2' : '5DB3',
},
]

#################
# Keypads: map to next number for every move[position]
# 1 2 3
# 4 5 6
# 7 8 9
keypad_p1 = {
    'U' : [None, 1, 2, 3, 1, 2, 3, 4, 5, 6 ],
    'D' : [None, 4, 5, 6, 7, 8, 9, 7, 8, 9 ],
    'L' : [None, 1, 1, 2, 4, 4, 5, 7, 7, 8 ],
    'R' : [None, 2, 3, 3, 5, 6, 6, 8, 9, 9 ],
}
#     1
#   2 3 4
# 5 6 7 8 9
#   A B C
#     D
keypad_p2 = {
    'U' : [None, 1, 2, 1, 4, 5,   2,   3,   4, 9,   6,   7,   8, 0xb ],
    'D' : [None, 3, 6, 7, 8, 5, 0xa, 0xb, 0xc, 9, 0xa, 0xd, 0xc, 0xd ],
    'L' : [None, 1, 2, 2, 3, 5,   5,   6,   7, 8, 0xa, 0xa, 0xb, 0xd ],
    'R' : [None, 1, 3, 4, 4, 6,   7,   8,   9, 9, 0xb, 0xc, 0xc, 0xd ],
}

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = ''
    pos_p1 = pos_p2 = 5
    for line in aoc_input.splitlines()  :
        for move in line :
            pos_p1 = keypad_p1[move][pos_p1]
            pos_p2 = keypad_p2[move][pos_p2]
        p1_result += f'{pos_p1}'
        p2_result += f'{pos_p2:X}'

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
