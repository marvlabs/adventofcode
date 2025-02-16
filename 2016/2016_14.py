#!python3
'''AoC 2016 Day 14'''
from hashlib import md5
import functools
import re
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '14',
    'url'           :   'https://adventofcode.com/2016/day/14',
    'name'          :   "One-Time Pad - MD5(MD5(MD5(MD5(...))))",
    'difficulty'    :   'D2',
    'learned'       :   'SEARCH. Not MATCH. Aaaaargh',
    't_used'        :   '20',
    'result_p1'     :   23769,
    'result_p2'     :   20606,
}
#############
TESTS = [
{
        'name'  : 'md5_abc',
        'input' : '''abc''',
        'p1' : 22728,
        'p2' : 22551,
},
]

#################

@functools.cache
def get_hash(salt, id, key_stretch = 0) :
    h = md5(f'{salt}{id}'.encode()).hexdigest()
    for _ in range(key_stretch) :
        h = md5(h.encode()).hexdigest()
    return h


match3 = re.compile(r'(.)\1\1')
assert match3.search('abcccd').start() == 2
assert not match3.search('abccdd')
assert 'cc38887a5' in md5('abc18'.encode()).hexdigest()

def find_next_hash(salt, id, key_stretch=0) :
    while True :
        hash = get_hash(salt, id, key_stretch)
        if matched := match3.search(hash) :
            match5 = matched.group(1) * 5
            
            for i in range(1,1001) :
                confirm_hash = get_hash(salt, id+i, key_stretch)
                if match5 in confirm_hash :
                    return id
        id += 1


def solve(aoc_input, part1=True, part2=True, attr=None) :

    get_hash.cache_clear()
    id = -1
    for _ in range(64) :
        id = find_next_hash(aoc_input.strip(), id+1)
    p1_result = id

    get_hash.cache_clear()
    id = -1
    for j in range(64) :
        id = find_next_hash(aoc_input.strip(), id+1, 2016)
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
