#!python3
'''AoC 2016 Day 01'''
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '01',
    'url'           :   'https://adventofcode.com/2016/day/01',
    'name'          :   "No Time for a Taxicab - run left and right",
    'difficulty'    :   'D1',
    'learned'       :   'Small steps are better than big jumps',
    't_used'        :   '30',
    'result_p1'     :   209, 
    'result_p2'     :   136,
}
#############
TESTS = [
{
        'name'  : 'test12',
        'input' : '''R5, L5, R5, R3, R1, R1, R1, R1''',
        'p1' : 12,
        'p2' : 13,
},
{
        'name'  : 'test_p2',
        'input' : '''R8, R4, R4, R8''',
        'p1' : 8,
        'p2' : 4,
},
]

#################
dirs = {
    'N' : (0,-1),
    'S' : (0,1),
    'E' : (1,0),
    'W' : (-1,0),
}
turns = {
    'NR' : 'E',
    'ER' : 'S',
    'SR' : 'W',
    'WR' : 'N',
    'NL' : 'W',
    'WL' : 'S',
    'SL' : 'E',
    'EL' : 'N',
}

def run(pos, instructions) :
    dir = 'N'
    seen = set()
    first_double_pos = None

    for i in instructions :
        dir = turns[dir+i[0]]
        vec = dirs[dir]
        dist = int(i[1:])
        for d in range(dist) :
            pos = (pos[0] + vec[0], pos[1] + vec[1])
            if not first_double_pos and pos in seen :
                first_double_pos = pos
            seen.add(pos)

    return pos, first_double_pos


def solve(aoc_input, part1=True, part2=True, attr=None) :
    instructions = aoc_input.split(', ')
    endpos, double_pos = run((0,0), instructions)
    p1_result = abs(endpos[0]) + abs(endpos[1])
    p2_result = abs(double_pos[0]) + abs(double_pos[1])
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
