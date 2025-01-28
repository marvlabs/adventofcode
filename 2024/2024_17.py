#!python3
'''AoC 2024 Day 17'''
import re
import sys
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '17',
    'url'           :   'https://adventofcode.com/2024/day/17',
    'name'          :   "Chronospatial Computer: wtf is going on?",
    'difficulty'    :   'D3',
    'learned'       :   'Mhmmm, chronospatial debugging???',
    't_used'        :   '180',
    'result_p1'     :   '1,0,2,0,5,7,2,1,3',
    'result_p2'     :   265652340990875,
}
#############
TESTS = [
{
        'name'  : 'Alternate Testcase from somewhere',
        'input' : '''Register A: 12345678
Register B: 0
Register C: 0

Program: 2,4,1,3,7,5,0,3,1,4,4,4,5,5,3,0''',
        'p1' : '3,4,4,1,7,0,2,2',
        'p2' : 266926175730705,
},
{
        'name'  : 'Testprog',
        'input' : '''Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0''',
        'p1' : '4,6,3,5,6,3,5,2,1,0',
        'p2' : None,
},{
        'name'  : 'Self-Replication',
        'input' : '''Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0''',
        'p1' : None,
        'p2' : 117440,
},
]

#################
# Define Chronospatial Computer: Registers and Instruction, then an ALU which can run a program
# (all tests from the instructions can be found as asserts at the bottom of this file :) 
Registers = {
   'A' : 0,
   'B' : 0,
   'C' : 0,
   'IP' : 0,
   'OUT' : [],
}

def combo(operand) :
    if operand > 6 :sys.exit(f"Explode with operand {7}")
    if operand < 4: return operand
    return Registers[chr(ord('A') + operand - 4)]

def adv(c_op) : Registers['A'] = Registers['A'] // (2**combo(c_op))
def bxl(op)   : Registers['B'] = Registers['B'] ^ op
def bst(c_op) : Registers['B'] = combo(c_op) % 8
def jnz(op)   :
    if Registers['A'] != 0 : Registers['IP'] = op-2
def bxc(op)   : Registers['B'] = Registers['B'] ^ Registers['C']
def out(c_op) : Registers['OUT'].append(combo(c_op) % 8)
def bdv(c_op) : Registers['B'] = Registers['A'] // (2**combo(c_op))
def cdv(c_op) : Registers['C'] = Registers['A'] // (2**combo(c_op))
Instructions = [ adv, bxl, bst, jnz, bxc, out, bdv, cdv ]

def run(program) :
    Registers['IP'] = 0
    Registers['OUT'] = []
    while Registers['IP'] < len(program) :
        instruction = Instructions[ program[Registers['IP']] ]
        operand  = program[Registers['IP']+1]
        instruction( operand )
        Registers['IP'] += 2

#################
def solve(aoc_input, part1=True, part2=True, attr=None) :
    regs, program = ( list( map( int, re.findall( "-?\\d+", s ) ) ) for s in aoc_input.split( "\n\n" ) ) 

    Registers['A'], Registers['B'], Registers['C'] = regs
    run(program)
    p1_result = ','.join(map(str, Registers['OUT']))
    p2_result = find_a(program, len(program)-1, 0)

    return p1_result, p2_result


# My input program:
# 2,4,1,7,7,5,0,3,1,7,4,1,5,5,3,0
# bst 4  REG-B % 8        -> REG-B      only least 3 bit of B significant (and initial value not relevant)
# bxl 7  REG-B ^ 7        -> REG-B      invert them
# cdv 5  REG-A / 2**REG-B -> REG-C      C gets some value (initial value not relevant)
# adv 3  REG-A / 8        -> REG-A      A gets smaller -> 8 values will produce the same next value
# bxl 7  REG-B ^ 7        -> REG-B      B xor 111 -> invert
# bxc 1  REG-B ^ REG-C    -> REG-B      B xor C
# out 5  REG-B % 8        -> OUT        lower 3 bit of B
# jnz 0  REG-A != 0       -> IP 0       (loop until A == 0)

# RevEng : tracing the 16 cycles to understand what happens, then code a reverse search
# RUNNING:  0 bst 4 {'A': 265652340990875,  'B': 0, 'C': 0, 'IP': 0, 'OUT': []}
# RUNNING:  0 bst 4 {'A': 33206542623859,  'B': 0, 'C': 0, 'IP': 0, 'OUT': [2]}
# RUNNING:  0 bst 4 {'A': 4150817827982,  'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4]}
# RUNNING:  0 bst 4 {'A': 518852228497,  'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1]}
# RUNNING:  0 bst 4 {'A': 64856528562,  'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7]}
# RUNNING:  0 bst 4 {'A': 8107066070,  'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7, 7]}
# RUNNING:  0 bst 4 {'A': 1013383258, 'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7, 7, 5]}
# RUNNING:  0 bst 4 {'A': 126672907, 'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7, 7, 5, 0]}
# RUNNING:  0 bst 4 {'A': 15834113, 'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7, 7, 5, 0, 3]}
# RUNNING:  0 bst 4 {'A': 1979264, 'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7, 7, 5, 0, 3, 1]}
# RUNNING:  0 bst 4 {'A': 247408, 'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7, 7, 5, 0, 3, 1, 7]}
# RUNNING:  0 bst 4 {'A': 30926, 'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7, 7, 5, 0, 3, 1, 7, 4]}
# RUNNING:  0 bst 4 {'A': 3865, 'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7, 7, 5, 0, 3, 1, 7, 4, 1]}
# RUNNING:  0 bst 4 {'A': 483, 'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7, 7, 5, 0, 3, 1, 7, 4, 1, 5]}
# RUNNING:  0 bst 4 {'A': 60, 'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7, 7, 5, 0, 3, 1, 7, 4, 1, 5, 5]}
# RUNNING:  0 bst 4 {'A': 7, 'B': 0, 'C': 0, 'IP': 0, 'OUT': [2, 4, 1, 7, 7, 5, 0, 3, 1, 7, 4, 1, 5, 5, 3]}
# FINISHED:         {'A': 0,'B': 0, 'C': 7, 'IP':16, 'OUT': [2, 4, 1, 7, 7, 5, 0, 3, 1, 7, 4, 1, 5, 5, 3, 0]}

# Try to find an A which produces the last value, then recurse backwards with all found A's
def find_a(program, idx, a_start) :
    if idx < 0 :
        #print (f'Found an a {a_start}')
        return a_start
    found = 0
    for i in range(8) :
        a = a_start*8 + i
        if a == 0 : continue
        Registers['A'] = a
        Registers['B'] = 0
        run(program)
        if Registers['OUT'][0] == program[idx] : 
            res = find_a(program, idx-1, a)
            if res and (found == 0 or res < found) : 
                found = res
    return found



# My first try was brute force...
# p2_result = find_a_for(program, program)
# No dice, nowhere near.
#
# Then I first tried exponetial a's until I found something which generates 16 output values.
# a = find_length(program, len(program))
# Letting that run gave me some cyclic info: every n iterations we would get a a better result
# Trying and testing different starting values gave me some more info, until a bit of tuning and patience found a result:
# p2_result = find_a_for(program, program, 35184660128667, 2097152)
# p2_result = find_a_for(program, program, 171790125704091, 2097152*1024)
#
# Checking what actually happens from a known solution finally gave me some understanding of how to reverse search for the solution.

# def find_length(program, l) :
#     for x in range(1000000) :
#         a = 2**x
#         Registers['A'] = a
#         Registers['B'] = 0
#         Registers['C'] = 0

#         run(program)
#         if len(Registers['OUT']) == l : 
#             print (f"Found length {l} at {a}")
#             return a

# # Brute forcing was a bit optimistic...
# def find_a_for(program, expected, start, step=1) :
#     for a in range(start, start+1000000000000000000000000000000000, step):
#         #if a % 10000000 == 0 : 
#         #print(a)
#         Registers['IP'] = 0
#         Registers['OUT'] = []
#         Registers['A'] = a
#         Registers['B'] = 0
#         Registers['C'] = 0
#
#         find_index = 0
#
#         while Registers['IP'] < len(program) :
#             instr = program[Registers['IP']]
#             Instructions[instr]['run']( program[Registers['IP']+1])
#             if instr == 5 :
#                 # we just outputed something
#                 if expected[find_index] != Registers['OUT'][find_index] :
#                     break
#                 find_index += 1
#                 if find_index > 11 : print(a, find_index)
#                 if find_index == len(expected) :
#                     return a


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    Registers['A'] = 35; Registers['B'] = 3; adv(5); assert Registers['A'] == 4
    Registers['A'] = 35; Registers['B'] = 3; adv(2); assert Registers['A'] == 8
    Registers['B'] = 15; bxl(5); assert Registers['B'] == 10
    Registers['B'] = 15; bst(5); assert Registers['B'] == 7
    Registers['A'] = 35; Registers['IP'] = 0; jnz(5); assert Registers['IP'] == 3
    Registers['A'] =  0; Registers['IP'] = 0; jnz(5); assert Registers['IP'] == 0
    Registers['B'] = 15; Registers['C'] = 5; bxc(42); assert Registers['B'] == 10
    Registers['A'] = 35; Registers['B'] = 3; bdv(5); assert Registers['B'] == 4
    Registers['A'] = 35; Registers['C'] = 3; cdv(6); assert Registers['C'] == 4

    Registers['C'] = 9; run([2,6]); assert Registers['B'] == 1
    Registers['A'] = 10; run([5,0,5,1,5,4]); assert all([a == b for a, b in zip(Registers['OUT'], [0,1,2])])
    Registers['A'] = 2024; run([0,1,5,4,3,0]); assert all([a == b for a, b in zip(Registers['OUT'], [4,2,5,6,7,7,7,7,3,1,0])]); assert Registers['A'] == 0
    Registers['B'] = 29; run([1,7]);  assert Registers['B'] == 26
    Registers['B'] = 2024; Registers['C'] = 43690; run([4,0]); assert Registers['B'] == 44354


    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
