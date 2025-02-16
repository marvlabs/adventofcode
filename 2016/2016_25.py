#!python3
'''AoC 2016 Day 25'''
import time
from copy import deepcopy
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
#################
# Define Computer: Registers and Instruction, then an ALU which can run a program
Registers = dict.fromkeys( ['a', 'b', 'c', 'd', 'IP', 'OUT'], 0 )
def value_or_register(s) : return s if isinstance(s, int) else Registers[s]
def cpy(x, y)   : Registers['IP'] += 1; Registers[y] = value_or_register(x)
def inc(x)      : Registers['IP'] += 1; Registers[x] += 1
def dec(x)      : Registers['IP'] += 1; Registers[x] -= 1
def jnz(x, rel) : Registers['IP'] += value_or_register(rel) if value_or_register(x) != 0 else 1
def reset() : 
    for r in Registers : Registers[r] = 0
    Registers['OUT'] = ''

ToggleMap = { 'inc' : 'dec', 'dec' : 'inc', 'tgl' : 'inc', 'jnz' : 'cpy', 'cpy' : 'jnz'}
def tgl(x, prog) :
    instr = Registers['IP'] + value_or_register(x)
    Registers['IP'] += 1
    if instr < 0 or instr >= len(prog) : return
    prog[instr][0] = ToggleMap[prog[instr][0]]
    #print(f"Assembunny Toggled {instr}")
    #for i, l in enumerate(prog): print(i, l)
    optimize(prog) # re-optimize the new program

def out(x) : Registers['IP'] += 1; Registers['OUT'] += f'{value_or_register(x)}'; return value_or_register(x)

def run(p, break_on_output=lambda:False) :
    program = deepcopy(p)
    optimize(program)
    start = time.time()
    count = 0
    while Registers['IP'] < len(program) :
        instruction, *operands = program[Registers['IP']]
        if instruction == 'tgl' : operands.append(program)
        ret = globals()[instruction](*operands)
        count += 1
        #if count % 1E9 == 0 : print(count)
        # If output was added: run the verify function to check for break condition
        if ret != None and break_on_output() : 
            return Registers['OUT']
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

def signal_wrong_or_achieved() :
    out = Registers['OUT']
    if len(out) > 20 : 
        return True
    for i in range(len(out)-1) :
        if (out[i] == '0' and out[i+1] != '1' ) or (out[i] == '1' and out[i+1] != '0') :
            return True
    return False

#################
def solve(aoc_input, part1=True, part2=True, attr=None) :
    program = [ s.split() for s in aoc_input.splitlines() ]

    a = 0
    while True :
        reset()
        Registers['a'] = a
        signal = run(program, signal_wrong_or_achieved)
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
