#!python3
'''AoC 2015 Day 23'''
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '23',
    'url'           :   'https://adventofcode.com/2015/day/23',
    'name'          :   "Opening the Turing Lock: another comp sim",
    'difficulty'    :   'D2',
    'learned'       :   '...and it worked, just like that...',
    't_used'        :   '60',
    'result_p1'     :   307,
    'result_p2'     :   160,
}
#############
TESTS = [
{
        'name'  : 'small prog',
        'input' : '''inc b
jio b, +2
tpl b
inc b''',
        'p1' : 2,
        'p2' : None,
},
]

#################
# Define Computer: Registers and Instruction, then an ALU which can run a program
Registers = {
   'a' : 0,
   'b' : 0,
   'IP' : 0,
}

def hlf(r)      : Registers['IP'] += 1; Registers[r] = Registers[r] // 2
def tpl(r)      : Registers['IP'] += 1; Registers[r] = Registers[r] * 3
def inc(r)      : Registers['IP'] += 1; Registers[r] += 1
def jmp(rel)    : Registers['IP'] += int(rel)
def jie(r, rel) : Registers['IP'] += int(rel) if Registers[r] % 2 == 0 else 1
def jio(r, rel) : Registers['IP'] += int(rel) if Registers[r] == 1     else 1


def run(program) :
    while Registers['IP'] < len(program) :
        instruction, operands = program[Registers['IP']]
        globals()[instruction](*operands)

#################
def solve(aoc_input, part1=True, part2=True, attr=None) :
    program = []
    for s in aoc_input.splitlines() :
        if s == '' : continue
        instruction, op = s.split(' ', 1)
        ops = op.split(',')
        program.append( (instruction, ops) )

    Registers['IP'] = 0; Registers['a'] = 0; Registers['b'] = 0
    run(program)
    p1_result = Registers['b']

    Registers['IP'] = 0; Registers['a'] = 1; Registers['b'] = 0
    run(program)
    p2_result = Registers['b']

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    # Tests for Computer implementation:
    Registers['IP'] = 0; Registers['a'] = 2; Registers['b'] = 7; 
    hlf('a'); hlf('b'); assert Registers['a'] == 1; assert Registers['b'] == 3
    tpl('a'); tpl('b'); assert Registers['a'] == 3; assert Registers['b'] == 9
    inc('a'); inc('b'); assert Registers['a'] == 4; assert Registers['b'] == 10
    assert Registers['IP'] == 6
    jmp("+3"); jmp("-1"); assert Registers['IP'] == 8

    Registers['IP'] = 5; Registers['a'] = 1; Registers['b'] == 6
    jie('a', "+4"); assert Registers['IP'] == 6
    jie('b', "+4"); assert Registers['IP'] == 10
    jio('a', "+2"); assert Registers['IP'] == 12
    jio('b', "+2"); assert Registers['IP'] == 13

    Registers['IP'] = 0; Registers['a'] = 0; Registers['b'] = 0; 
    prog = [ 
        ('inc', ('a',)), 
        ('jio', ('a', +2)), 
        ('tpl', ('a',)), 
        ('inc', ('a',)), 
    ]
    run(prog)
    assert Registers['a'] == 2

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
