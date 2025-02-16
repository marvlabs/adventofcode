#!python3
'''AoC 2016 Day 25'''
from assembunny import Assembunny
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '25',
    'url'           :   'https://adventofcode.com/2015/day/25',
    'name'          :   "Clock Signal - Assembunny generator",
    'difficulty'    :   'D2',
    'learned'       :   'careful change does it',
    't_used'        :   '20',
    'result_p1'     :   198,
    'result_p2'     :   0,
}
#############
TESTS = [
]

#################
# Add 'out x' to Assembunny (day 12, 23)
# Add verify function to check output for break condition

def signal_wrong_or_achieved(bunny) :
    out = bunny.get('OUT')
    if len(out) > 20 : 
        return True
    for i in range(len(out)-1) :
        if (out[i] == '0' and out[i+1] != '1' ) or (out[i] == '1' and out[i+1] != '0') :
            return True
    return False

#################
def solve(aoc_input, part1=True, part2=True, attr=None) :
    bunny = Assembunny(aoc_input, do_optimize=True)

    a = 0
    while True :
        bunny.reset()
        bunny.set('a', a)
        signal = bunny.run(break_on_output=signal_wrong_or_achieved)
        if len(signal) > 20 :
            p1_result = a
            break
        a += 1

    return p1_result, 0

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
