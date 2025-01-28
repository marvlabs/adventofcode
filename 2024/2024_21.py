#!python3
'''AoC 2024 Day 21'''
import functools
from itertools import permutations
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '21',
    'url'           :   'https://adventofcode.com/2024/day/21',
    'name'          :   "Keypad Conundrum: Robo Cascade",
    'difficulty'    :   'D3',
    'learned'       :   'What??? How??? ...and so many errors...',
    't_used'        :   '120',
    'result_p1'     :   179444,
    'result_p2'     :   223285811665866,
}
#############
TESTS = [
{
'name'  : 'Testcodes',
'input' : '''029A
980A
179A
456A
379A''',
'p1' : 126384,
'p2' : 154115708116294,
},

]

#################
keypad = {
    '7': (0,0),
    '8': (1,0),
    '9': (2,0),
    '4': (0,1),
    '5': (1,1),
    '6': (2,1),
    '1': (0,2),
    '2': (1,2),
    '3': (2,2),
    '0': (1,3),
    'A': (2,3),
}
robopad = {
    '^': (1,0),
    'A': (2,0),
    '<': (0,1),
    'v': (1,1),
    '>': (2,1),
}
moves = {
    '^': (0,-1),
    'v': (0,1),
    '<': (-1,0),
    '>': (1,0),
}

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0
    shortest.cache_clear()

    for code in aoc_input.splitlines() :
        p1_result += shortest(code, True, 3) * int(code[:-1])
        p2_result += shortest(code, True, 26) * int(code[:-1])

    return p1_result, p2_result


@functools.cache
def shortest(code, use_kp, depth) :
    pad = keypad if use_kp else robopad
    seq_len = 0
    pos = pad['A']

    for c in code :
        diff_x = pad[c][0] - pos[0]
        diff_y = pad[c][1] - pos[1]
        keys  = abs(diff_x) * ('<' if diff_x < 0 else '>')
        keys += abs(diff_y) * ('^' if diff_y < 0 else 'v')
        if depth == 1 :
            # We don't care about the order on the outermost level.
            seq_len += len(keys)+1 # add the 'A' length
        else :
            # Try all valid sequences which navigate to this button
            min_len = None
            for perm in set(permutations(keys)):
                if moves_nok(pad, pos, perm) : continue
                s = shortest(''.join(perm) + 'A', False, depth-1)
                min_len = s if not min_len or s < min_len else min_len
            seq_len += min_len 
        pos = pad[c]

    return seq_len

assert shortest('029A', True, 1) == len('<A^A>^^AvvvA')

# Don't move over empty space
def moves_nok(pad, pos, seq) :
    x, y = pos
    for c in seq :
        x += moves[c][0]
        y += moves[c][1]
        if (x,y) not in pad.values() :return True
    return False

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
