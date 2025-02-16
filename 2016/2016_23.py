#!python3
'''AoC 2016 Day 23'''
from assembunny import Assembunny
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '23',
    'url'           :   'https://adventofcode.com/2015/day/23',
    'name'          :   "Safe Cracking - Assembunny self morph",
    'difficulty'    :   'D3',
    'learned'       :   'Assembunny Optimization, yeah!!!',
    't_used'        :   '90',
    'result_p1'     :   11662,
    'result_p2'     :   479008222,
}
#############
TESTS = [
{
        'name'  : 'small prog',
        'input' : '''cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a''',
        'p1' : 42,
        'p2' : None,
},
{
        'name'  : 'tgl prog',
        'input' : '''cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a''',
        'p1' : 3,
        'p2' : None,
},

{
        'name'  : 'end-prog',
        'input' : '''cpy -16 c
cpy 1 c
cpy 86 c
cpy 77 d
inc a
dec d
jnz d -2
dec c
jnz c -5
''',
        'p1' : 6629,
        'p2' : None,
},
]

#################
# This puzzle extends Assembunny (day 12) with tgl self morphing technology - this helps hiding the code's intent
# The provided program computes the factorial of the 'a' input and adds an offset (86*77 in my case) to the result (see end-prog test above)
# The existing interpreter works, the results are correct. But. Performance.
# As Assembunny V2 still lacks add and mul operations, everything is computed in looped increments.
# Running as provided, it takes more than half an hour on my M2 Pro:
# No opt  : 2217s, Assembunny hopped 3,501,374,000 times (1.58 MHops) 
# Some optimization required:
# Adding add and mul to the computer, the program can be 'optimized'
# (nop helps to not have to change jnz offsets, but makes it slower)
# ADD NOP : 1113s, Assembunny hopped 2,064,369,236 times (1.85 MHops)
# ADD     :  913s, Assembunny hopped 1,376,252,948 times (1.51 MHops)
# MUL     : 0.022, Assembunny hopped 20,382 times (1.89 MHops)
# We maybe need an automatic optimizer? Analyze the prog and detect add/mul loops???
# -> YES! Opimizer for mul and add brings runtime down to:
# MUL ADD : 0.000, Assembunny hopped 246 times (1.57 MHops) !!!
# Also backported to day 12 => runtime from 13s to 0, cycles from 28E6 to 400 :-)
# (BTW: tgl could fail if it would target optimized code. But it doesn't :-)
#################

#################
def solve(aoc_input, part1=True, part2=True, attr=None) :
    results = []
    for input_value in (7,12) :
        bunny = Assembunny(aoc_input, do_optimize=True)
        bunny.reset()
        bunny.set('a', input_value)
        bunny.run()
        results.append(bunny.get('a'))

    return results

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
