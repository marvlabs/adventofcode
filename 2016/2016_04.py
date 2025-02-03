#!python3
'''AoC 2016 Day 04'''
import re
from collections import Counter
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '04',
    'url'           :   'https://adventofcode.com/2016/day/04',
    'name'          :   "Security Through Obscurity - mangled room names",
    'difficulty'    :   'D2',
    'learned'       :   'sort key functions',
    't_used'        :   '30',
    'result_p1'     :   158835, 
    'result_p2'     :   993,
}
#############
TESTS = [
{
        'name'  : 'sometest',
        'input' : '''aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]''',
        'p1' : 1514,
        'p2' : None,
},
]
#############

def verify_room(name, nr, hash) :
    count = Counter(name)
    del count['-']

    h = ''.join( [ c for c in sorted(count, key=lambda x: (-count[x], x)) ] )
    return nr if h[:5] == hash else 0


rotate_char = lambda c, i : chr(((ord(c) - ord('a')) + i) % 26  + ord('a')) 
rotate_name = lambda name, i : ''.join( [ ' ' if c == '-' else rotate_char(c, i) for c in name ] )
assert rotate_name('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = 0
    for string in aoc_input.splitlines()  :
        name, nr, hash = re.match(r'(.*)-(\d+)\[(.*)\]', string).groups()
        id = int(nr)

        p1_result += verify_room(name, id, hash)
        if 'north' in rotate_name(name, id) :
            p2_result = id

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
