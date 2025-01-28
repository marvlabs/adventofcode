#!python3
'''AoC 2024 Day 19'''
import functools
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '19',
    'url'           :   'https://adventofcode.com/2024/day/19',
    'name'          :   "Linen Layout: too many towels",
    'difficulty'    :   'D2',
    'learned'       :   'CLEAR THE F***ING CACHE. Or else.',
    't_used'        :   '30',
    'result_p1'     :   369,
    'result_p2'     :   761826581538190,
}
#############
TESTS = [
 {
'name'  : 'Linens-1',
'input' : '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
''',
'p1' : 6,
'p2' : 16,
    },
]

#################
linens = []

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0
    linen_str, patterns = aoc_input.split( "\n\n" )
    linens.clear()
    linens.extend(linen_str.split(", "))

    valid_pattern.cache_clear()
    for pattern in patterns.splitlines() :
        valid = valid_pattern(pattern)
        p1_result += 1 if valid else 0
        p2_result += valid

    return p1_result, p2_result

@functools.cache
def valid_pattern(pattern) :
    variations = 0
    for p in linens :
        if pattern.startswith(p) :
            if len(p) == len(pattern) :
                variations += 1
            else :
                variations += valid_pattern(pattern[len(p):])
    return variations

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
