#!python3
'''AoC 2016 Day 23'''
import time
from copy import deepcopy
#from math import factorial
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
# The interpreter works, the results are correct. But. Performance.
# As Assembunny V2 here lacks add and mul operations, everything is looped increments.
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
# Define Computer: Registers and Instruction, then an ALU which can run a program
Registers = dict.fromkeys( ['a', 'b', 'c', 'd', 'IP'], 0 )
def value_or_register(s) : return s if isinstance(s, int) else Registers[s]
def cpy(x, y)   : Registers['IP'] += 1; Registers[y] = value_or_register(x)
def inc(x)      : Registers['IP'] += 1; Registers[x] += 1
def dec(x)      : Registers['IP'] += 1; Registers[x] -= 1
def jnz(x, rel) : Registers['IP'] += value_or_register(rel) if value_or_register(x) != 0 else 1
def reset() : 
    for r in Registers : Registers[r] = 0

ToggleMap = { 'inc' : 'dec', 'dec' : 'inc', 'tgl' : 'inc', 'jnz' : 'cpy', 'cpy' : 'jnz'}
def tgl(x, prog) :
    instr = Registers['IP'] + value_or_register(x)
    Registers['IP'] += 1
    if instr < 0 or instr >= len(prog) : return
    prog[instr][0] = ToggleMap[prog[instr][0]]
    #print(f"Assembunny Toggled {instr}")
    #for i, l in enumerate(prog): print(i, l)
    optimize(prog) # re-optimize the new program

def run(p) :
    program = deepcopy(p)
    optimize(program)
    start = time.time()
    count = 0
    while Registers['IP'] < len(program) :
        instruction, *operands = program[Registers['IP']]
        if instruction == 'tgl' : operands.append(program)
        globals()[instruction](*operands)
        count += 1
        #if count % 1E9 == 0 : print(count)
    used = time.time() - start
    print (f"Assembunny hopped {count:,d} times ({count / used / 1E6:.2f} MHops)")

#######################################
# Optimizer: add y to reg x -> reg x
def add(x, y)      : Registers['IP'] += 1; Registers[x] += value_or_register(y)
# Optimizer: multiply reg x by y -> reg x
def mul(x, y)      : Registers['IP'] += 1; Registers[x] *= value_or_register(y)
# Optimizer: do nothing -> not having to adjust jump offset if used to fill gaps after optimizing
def nop()          : Registers['IP'] += 1

# Find optimizations in programs:
# - pre-compile numbers
# - multiply-add : inc reg1 / dec reg2 / jnz reg2 -2 / dec reg3 / jnz reg3 -5 => mul reg2 reg3 / add reg1 reg2 / cpy 0 reg2 / cpy 0 reg3 / nop
# - add          : inc a / dec b / jnz b -2 => add a b / cpy 0 b / nop
def optimize(p) :
    # INTs -> pre-compile to numbers if not a register
    for instr in range(len(p)) :
        for attr_nr in range(1,len(p[instr])) :
            try: p[instr][attr_nr] = int(p[instr][attr_nr])
            except ValueError: pass

    # Multipliy-add
    for i in range(len(p) - 4) :
        inc1, dec2, jnz2, dec3, jnz3 = p[i:i+5]
        if inc1[0] == 'inc' and dec2[0] == dec3[0] == 'dec' and jnz2[0] == jnz3[0] == 'jnz' \
                and dec2[1] == jnz2[1] and dec3[1] == jnz3[1] \
                and inc1[1] != dec2[1] and dec3[1] != dec2[1]\
                and jnz2[2] == -2 and jnz3[2] == -5 :
            p[i]   = ['mul', dec2[1], dec3[1]]
            p[i+1] = ['add', inc1[1], dec2[1]]
            p[i+2] = ['cpy', 0, dec2[1]]
            p[i+3] = ['cpy', 0, dec3[1]]
            p[i+4] = ['nop',]
            #print(f"Optimizer MULT at", i)
    # Add
    for i in range(len(p) - 2) :
        inc1, dec2, jnz2 = p[i:i+3]
        if inc1[0] == 'inc' and dec2[0] == 'dec' and jnz2[0] == 'jnz' \
                and dec2[1] == jnz2[1] \
                and inc1[1] != dec2[1] \
                and jnz2[2] == -2 :
            p[i]   = ('add', inc1[1], dec2[1])
            p[i+1] = ('cpy', 0, dec2[1])
            p[i+2] = ('nop',)
            #print(f"Optimizer ADD at", i)
#######################################

#################
def solve(aoc_input, part1=True, part2=True, attr=None) :
    program = [ s.split() for s in aoc_input.splitlines() ]

    reset()
    Registers['a'] = 7
    run(program)
    p1_result = Registers['a']

    reset()
    Registers['a'] = 12
    run(program)
    p2_result = Registers['a']
    #assert p2_result == factorial(12)+ 86*77

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
