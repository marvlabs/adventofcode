#!python3
from pprint import pprint as pp
import re
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '07',
    'url'           :   'https://adventofcode.com/2015/day/7',
    'name'          :   "Some Assembly Required - Wired Gates",
    'difficulty'    :   'D2',
    'learned'       :   'Python lists and dicts',
    't_used'        :   '90',
    'result_p1'     :   16076,
    'result_p2'     :   2797,
}
#############
TESTS = [
 {
        'name'  : 'circuit-1',
        'input' : '''
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
h -> a
''',
        'p1' : 65412,
        'p2' : None,
    },
]

#############

operations = {
    'AND'   : lambda x,y : (x & y) &0xffff,
    'OR'    : lambda x,y : (x | y) &0xffff,
    'XOR'   : lambda x,y : (x ^ y) &0xffff,
    'LSHIFT': lambda x,n : (x << n) &0xffff,
    'RSHIFT': lambda x,n : (x >> n) &0xffff,
    'NOT'   : lambda x,d : (~x) &0xffff,
    'VAL'   : lambda x,d : (x) &0xffff,
}

#################
def parse_gate(cmd, wirename) :
    gate = dict(wire=wirename, value=None, to_x=[], to_y=[])
    cmd_list = cmd.split()

    # VALUE (123 -> x, h -> a)
    if len(cmd_list) == 1 :
        arg1 = cmd_list[0]
        gate['op'] = 'VAL'
        gate['y'] = None
        gate['y_val'] = None
        if arg1.isdigit() :
            gate['x'] = None
            gate['x_val'] = int(arg1)
        else :
            gate['x'] = arg1
            gate['x_val'] = None
    # NOT (NOT x -> h)
    elif len(cmd_list) == 2 :
        arg1 = cmd_list[1]
        gate['op'] = 'NOT'
        gate['x'] = arg1
        gate['x_val'] = None
        gate['y'] = None
        gate['y_val'] = None
    # x OP y (x LSHIFT 2 -> f, x OR y -> e)
    elif len(cmd_list) == 3 :
        arg1 = cmd_list[0]
        arg2 = cmd_list[2]
        gate['op'] = cmd_list[1]
        if arg1.isdigit() :
            gate['x'] = None
            gate['x_val'] = int(arg1)
        else :
            gate['x'] = arg1
            gate['x_val'] = None
        if arg2.isdigit() :
            gate['y'] = None
            gate['y_val'] = int(arg2)
        else :
            gate['y'] = arg2
            gate['y_val'] = None
    
    return gate


def is_runnable(gate) :
    '''True if enough inputs are set for the gate to compute'''
    return  ((gate['x'] is None) or (gate['x_val'] is not None)) \
        and ((gate['y'] is None) or (gate['y_val'] is not None))


def wire_gates (gates) :
    '''Process all gates: add them to the "notify" list of the gate controling the inputs
       and check if immediately runnable (all inputs set)'''
    run_stack = []
    for gate in gates.values() :
        inputX = gate['x']
        inputY = gate['y']
        if inputX is not None :
            gates[inputX]['to_x'].append(gate)
        if inputY is not None :
            gates[inputY]['to_y'].append(gate)
        if is_runnable(gate) :
            run_stack.append(gate)
    return run_stack


def reset_gates (gates) :
    '''Init again for part 2 run'''
    for gate in gates.values() :
        gate['value'] = None
        if gate['x'] is not None :
            gate['x_val'] = None
        if gate['y'] is not None :
            gate['y_val'] = None


def run_gates(run_stack) :
    '''Compute all gates which are ready (have their inputs set). Notify the connected gates of the result, add them to the run queue if ready now'''
    while run_stack :
        run_gate = run_stack.pop()
        gate_result = operations[run_gate['op']](run_gate['x_val'], run_gate['y_val'])
        #print ('running ', run_gate['wire'], '->', gate_result)
        run_gate['value'] = gate_result
        for waiting_gate in run_gate['to_x'] :
            waiting_gate['x_val'] = gate_result
            if is_runnable(waiting_gate) :
                run_stack.append(waiting_gate)
        for waiting_gate in run_gate['to_y'] :
            waiting_gate['y_val'] = gate_result
            if is_runnable(waiting_gate) :
                run_stack.append(waiting_gate)


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = None, None
    gates = {}

    for string in aoc_input.splitlines()  :
        if string == '' : continue
        cmd, wirename = re.match('(.*) -> (\w+)', string).groups()
        gates[wirename] = parse_gate(cmd, wirename)

    run_stack_p1 = wire_gates(gates)
    run_stack_p2 = run_stack_p1.copy() # For part 2 run
    
    run_gates(run_stack_p1)
    p1_result = gates['a']['value']

    if part2 :
        reset_gates(gates)
        gates['b']['x_val'] = p1_result
        run_gates(run_stack_p2)
        p2_result = gates['a']['value']

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    assert operations['AND'](123,456) == 72
    assert operations['OR'](123,456) == 507
    assert operations['LSHIFT'](123,2) == 492
    assert operations['RSHIFT'](456,2) == 114
    assert operations['NOT'](123,None) == 65412
    assert operations['NOT'](456,None) == 65079
    assert operations['VAL'](42,None) == 42

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)

