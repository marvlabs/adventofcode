#!python3
import hashlib
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '04',
    'url'           :   'https://adventofcode.com/2015/day/4',
    'name'          :   'The Ideal Stocking Stuffer - Hash it',
    'difficulty'    :   'D1',
    'learned'       :   'Python MD5, string slice',
    't_used'        :   '15',
    'result_p1'     :   254575,
    'result_p2'     :   1038736,
}
#############
TESTS = [
    {
        'name'  : 'MD5-1',
        'input' : 'abcdef',
        'p1' : 609043,
        'p2' : None,
    },
    {
        'name'  : 'MD5-2',
        'input' : 'pqrstuv',
        'p1' : 1048970,
        'p2' : None,
    },
]
#############
def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1 = findMd5WithLeading(aoc_input, '00000') if part1 else None
    p2 = findMd5WithLeading(aoc_input, '000000') if part2 else None
    return p1, p2


def findMd5WithLeading(clear, leading) :
    idx = 0
    while True :
        idx += 1
        input = clear + str(idx)
        md5 = hashlib.md5(input.encode('utf-8')).hexdigest()
        if (md5[:len(leading)] == leading) :
            return idx

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
