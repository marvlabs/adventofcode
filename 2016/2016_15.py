#!python3
'''AoC 2016 Day 15'''
import re
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '15',
    'url'           :   'https://adventofcode.com/2016/day/15',
    'name'          :   "Timing is Everything - align them slots",
    'difficulty'    :   'D1',
    'learned'       :   'Optimized brute force... Should do Chinese-Remainder-Theorem',
    't_used'        :   '20',
    'result_p1'     :   317371, 
    'result_p2'     :   2080951,
}
#############
TESTS = [
{
    'name'  : '2Discs',
    'input' : 
'''Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.''',
    'p1' : 5,
    'p2' : None,
},
]

#################
# Optimized later: as soon as a slot is hit, increment the search loop by the product of the periods of the discs
def loop_till_zero(discs) :
    disc_found = 0
    interval = 1
    i = 0
    while True :
        for disc in discs :
            if (disc[2] + i + disc[0]) % disc[1] != 0 : break
            if disc[0] > disc_found :
                disc_found = disc[0]
                interval *= disc[1]
        else : return i # Wow: for ...else ! It's run when the for loop has finished (unbroken). Cool, saves a bool
        
        i += interval

def solve(aoc_input, part1=True, part2=True, attr=None) :
    discs = [ (disc, n, pos) for disc, n, _, pos in [ list(map(int, re.findall(r'\d+', line))) for line in aoc_input.splitlines() ] ]

    p1_result = loop_till_zero(discs)
    discs.append((len(discs)+1, 11, 0))
    p2_result = loop_till_zero(discs)

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
