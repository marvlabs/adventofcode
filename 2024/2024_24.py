#!python3
'''AoC 2024 Day 24'''
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '24',
    'url'           :   'https://adventofcode.com/2024/day/24',
    'name'          :   "Crossed Wires:",
    'difficulty'    :   'D3',
    'learned'       :   'Tedious inspections',
    't_used'        :   '180',
    'result_p1'     :   51657025112326,
    'result_p2'     :   'gbf,hdt,jgt,mht,nbf,z05,z09,z30',
}
#############
TESTS = [
{
    'name'  : 'T1',
    'input' : '''x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02''',
    'p1' : 4,
    'p2' : None,
},

{
    'name'  : 'T2',
    'input' : '''x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj''',
    'p1' : 2024,
    'p2' : None,
},]
#################

functions = {
    'AND' : lambda x, y : x & y,
    'OR' : lambda x, y : x | y,
    'XOR' : lambda x, y : x ^ y,
}

# ADD gates:
# OUT:   S = A ^ B ^ Cin;
# CARRY: C = (A & B) | ((A ^ B) & Cin);

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0
    gates = {}
    wires = {}
    feeds_into = {}
    inital_checks = []

    wirestr, gatestr = aoc_input.split( "\n\n" )

    for line in gatestr.splitlines()  :
        g1, func, g2, _, wire = line.split()
        gates[wire] = { 'i1' : g1, 'i2' : g2, 'f' : func }
        feeds_into[g1] = feeds_into.get(g1, []) + [wire]
        feeds_into[g2] = feeds_into.get(g2, []) + [wire]


    #wires = { w : int(s) for line in wirestr.splitlines() for w, s in line.split(': ') }
    for line in wirestr.splitlines() :
        w, s = line.split(': ')
        wires[w] = int(s)
        inital_checks.extend(feeds_into[w])

    run_gates(gates, feeds_into, wires, inital_checks)
    p1_result = sum ( 2**int(gate[1:]) for gate, val in wires.items() if gate[0] == 'z' and val == 1 ) 

    if part2 :
        in_bits_1 = sum(1 for gate in wires.keys() if gate[0] == 'x')
        in_bits_2 = sum(1 for gate in wires.keys() if gate[0] == 'y')
        out_bits  = sum(1 for gate in gates.keys() if gate[0] == 'z')
        assert in_bits_1 == in_bits_2 == out_bits-1
        
        failure_bits = test_some_adds(gates, feeds_into, inital_checks, in_bits_1)
        print("Failed bits in add test: ", failure_bits)
        # for i in failure_bits :
        #     involved_gates = find_gates_for_output_bit(gates, feeds_into, i)
        #     print (involved_gates)
        for i in range(in_bits_1) :
            print(f'{i:01d}', find_logic_for_wire(gates, feeds_into, f'z{i:02d}', 3))

        gates_fixed = fix_errors(gates, in_bits_1)
        assert test_some_adds(gates, feeds_into, inital_checks, in_bits_1) == set()
        p2_result = ','.join(sorted(gates_fixed))

    return p1_result, p2_result

def fix_errors(gates, bits) :
    swapped = []
    c_in = None

    for i in range(bits) :
        a_xor_b = find_gate(gates, f'x{i:02d}', f'y{i:02d}', 'XOR')
        a_and_b = find_gate(gates, f'x{i:02d}', f'y{i:02d}', 'AND')
        assert a_xor_b and a_and_b

        if not c_in :
            c_and_xor = None
            next_carry = a_and_b
            out = a_xor_b
        else :
                

            c_and_xor = find_gate(gates, c_in, a_xor_b, 'AND')
            if not c_and_xor :
                #c_and_xor = find_other_gate_input(gates, c_in, 'AND')
                print(f'FIX swap {a_and_b} and {a_xor_b}')
                swapped.extend(swap(gates , a_xor_b, a_and_b))
                gn = a_and_b
                a_and_b = a_xor_b
                a_xor_b = gn
            c_and_xor = find_gate(gates, c_in, a_xor_b, 'AND')

            if a_and_b[0] == 'z' :
                a_and_b_should_be = find_other_gate_input(gates, c_and_xor, 'OR')
                swapped.extend(swap(gates, a_and_b, a_and_b_should_be))
                print(f'FIX swap {a_and_b} and {a_and_b_should_be}')
                a_and_b = a_and_b_should_be

            next_carry = find_gate(gates, a_and_b, c_and_xor, 'OR')
            if next_carry :
                if next_carry[0] == 'z' and i < 44:
                    next_carry_should_be = find_gate(gates, c_in, a_xor_b, 'XOR')
                    swapped.extend(swap(gates, next_carry, next_carry_should_be))
                    print(f'FIX swap {next_carry} and {next_carry_should_be}')
                    next_carry = next_carry_should_be

            out = find_gate(gates, c_in, a_xor_b, 'XOR')

            print(f'Bit {i:02d}: XOR {a_xor_b} and AND {a_and_b}, c_and_xor {c_and_xor}, out {out}, next carry is {next_carry}')
            if (out[0] != 'z') :
                swapped.extend(swap(gates, out, c_and_xor))
                print(f'FIX swap {out} and {c_and_xor}')
                c_and_xor = out
                out = find_gate(gates, c_in, a_xor_b, 'XOR')
                c_and_xor = find_gate(gates, c_in, a_xor_b, 'AND')
                next_carry = find_gate(gates, a_and_b, c_and_xor, 'OR')
                print(f'FIX {i:02d}: XOR {a_xor_b} and AND {a_and_b}, c_and_xor {c_and_xor}, out {out}, next carry is {next_carry}')

        c_in = next_carry

    return swapped

def swap(gates, g1, g2) :
    g = gates[g1]
    gates[g1] = gates[g2]
    gates[g2] = g
    return [g1, g2]

def find_other_gate_input(gates, i, op) :
    for name, gate in gates.items() :
        if gate['i1'] == i  and gate['f'] == op :
            return gate['i2']
        if gate['i2'] == i  and gate['f'] == op :
            return gate['i1']
    return None

def find_gate(gates, i1, i2, op) :
    for name, gate in gates.items() :
        if ((gate['i1'] == i2 and gate['i2'] == i1) or (gate['i1'] == i1 and gate['i2'] == i2 )) and gate['f'] == op :
            return name
    return None

def find_gates_for_output_bit (gates, feeds_into, bit) :
    #print(f'finding gates for bit {bit}')
    gate = f'z{bit:02d}'
    inputs = set()
    to_check = [gates[gate]['i1'], gates[gate]['i2']]

    while len(to_check) :
        check = to_check.pop()
        inputs.add(check)
        if check[0] in 'xy': continue
        to_check.extend([gates[check]['i1'], gates[check]['i2']])
        
    return inputs

def find_logic_for_wire (gates, feeds_into, wire, depth=100) :
    #print(f'finding logic for wire {wire}')
    if depth == 0 : return wire

    in1 = gates[wire]['i1']
    in2 = gates[wire]['i2']
    logic_1 = in1 if in1[0] in 'xy' else f'[{in1}]{find_logic_for_wire(gates, feeds_into, in1, depth-1)}'
    logic_2 = in2 if in2[0] in 'xy' else f'[{in2}]{find_logic_for_wire(gates, feeds_into, in2, depth-1)}'
    return f"( {logic_1}  {gates[wire]['f']}  {logic_2} )"


def test_some_adds(gates, feeds_into, inital_checks, bits) :
    provoked_failures = set()
    for i in range(bits) :
        x = 2**i
        for a, b in [ (x, 0), (0, x), (x, x) ] :
            if add(gates, feeds_into, inital_checks, a, b, bits) != a+b :
                #print(f'Failure on add one bit {i:02d}')
                provoked_failures.add(i)
    
    return provoked_failures


def add(gates, feeds_into, inital_checks, o1, o2, bits) :
    wires = {}
    for i in range(bits) :
        wires[f'x{i:02d}'] = (o1 & (1<<i)) >> i
        wires[f'y{i:02d}'] = (o2 & (1<<i)) >> i
    
    run_gates(gates, feeds_into, wires, inital_checks)
    return sum ( 2**int(gate[1:]) for gate, val in wires.items() if gate[0] == 'z' and val == 1 )


def run_gates (gates, feeds_into, wires, inital_checks) :
    to_check = inital_checks.copy()
    while len(to_check) > 0 :
        w = to_check.pop()
        if w in wires : continue
        i1 = gates[w]['i1']
        i2 = gates[w]['i2']
        if i1 not in wires or i2 not in wires : continue

        wires[w] = functions[gates[w]['f']]( wires[i1], wires[i2] )
        if w in feeds_into : to_check.extend(feeds_into[w])





#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
