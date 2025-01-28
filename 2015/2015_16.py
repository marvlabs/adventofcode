#!python3
'''AoC 2015 Day 16'''
# from pprint import pprint as pp
import re
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '16',
    'url'           :   'https://adventofcode.com/2015/day/16',
    'name'          :   "Day 16: Aunt Sue - Who sent it",
    'difficulty'    :   'D1',
    'learned'       :   'Fill dict from regex',
    't_used'        :   '15',
    'result_p1'     :   103,
    'result_p2'     :   405,
}
#############
TESTS = [
]
#################
MFCSAM = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}


def filter_out_p1(aunts) :
    for aunt, things in aunts.items() :
        aunt_ok = True
        for thing, val in things.items() :
            if MFCSAM[thing] != val :
                aunt_ok = False
        if aunt_ok : return aunt
    return 0


def filter_out_p2(aunts) :
    for aunt, things in aunts.items() :
        aunt_ok = True
        for thing, val in things.items() :
            if thing in ['cats', 'trees'] : 
                if val <= MFCSAM[thing] :
                    aunt_ok = False
            elif thing in ['pomeranians', 'goldfish'] : 
                if val >= MFCSAM[thing] :
                    aunt_ok = False
            else :
                if MFCSAM[thing] != val :
                   aunt_ok = False

        if aunt_ok : return aunt
    return 0


def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    aunts = {
        name: { attr.strip(): int(val) for attr, val in [ attr_val.split(':') for attr_val in attrs.split(',') ] }
            for name, attrs in [ re.match(r'Sue (\d+): (.*)', l).groups() for l in aoc_input.splitlines()]
    }
    p1_result = filter_out_p1(aunts)
    p2_result = filter_out_p2(aunts)
    
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
