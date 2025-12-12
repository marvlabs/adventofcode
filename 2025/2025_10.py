#!python3
'''AoC 2025 Day 10'''
from itertools import combinations
from functools import reduce
from operator import xor
from scipy.optimize import linprog

#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '10',
    'url'           :   'https://adventofcode.com/2025/day/10',
    'name'          :   "Day 10: Factory - random bashing ALWAYS fixes things",
    'difficulty'    :   'D3',
    'learned'       :   'LP: scipy optimize for linear programming',
    't_used'        :   '120',
    'result_p1'     :   502,
    'result_p2'     :   21467,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
''',
        'p1' : 7,
        'p2' : 33,
    },
]
#################

# Every button (value is an xor mask) is either pressed once or not pressed at all.
# Try first all one-buttons, then all two-buttons combinations, etc up to all available buttons. Lowest press wins
def min_xor_presses(button_values, target) :
    for i in range(1, len(button_values)+1) :
        for c in combinations(button_values, i) :
            if reduce(xor, c) == target : return i


# Use linear programming solver
# https://en.wikipedia.org/wiki/Linear_programming
# https://docs.scipy.org/doc/scipy-1.15.2/reference/generated/scipy.optimize.linprog.html
def min_add_presses(buttons, joltages) :
    # Every button has a cost of 1 for a press
    costs = [1] * len(buttons) 

    # For each joltage: matrix for which button adds 1 to a joltage
    equation_matrix = [[(i in b)*1 for b in buttons] for i in range(len(joltages))] 
    
    #print (f'Testing linprog. costs={costs}\n   buttons={buttons}\n   eqs={equation_matrix}\n   jolts={joltages}')

    # This linprog module does magically solve for the minimum number of presses
    result = linprog(c=costs, A_eq=equation_matrix, b_eq=joltages, integrality=1)

    # check = {}
    # for b, n in zip(buttons, result.x) :
    #     print(f' {int(n):3} * [ { '   '.join([ str(i) if i in b else '-' for i in range(len(joltages)) ]) } ]')
    #     for j in b : check[j] = check.get(j, 0) + int(n)
    # print (f'Result: { [ val for key, val in sorted(check.items()) ]}  ===  {joltages} jolts')
    
    return int(result.fun)


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0
    for line in aoc_input.splitlines()  :
        ind_str, *button_strs, jolt_str = line.split()
        indicator_target = sum( ((c=='#')) * 2**i for i, c in enumerate(ind_str[1:-1]))
        buttons = [ list(map(int, btns[1:-1].split(','))) for btns in button_strs ]
        button_values = [ sum( 2**b for b in button ) for button in buttons ]
        joltages = list(map(int, jolt_str[1:-1].split(',')))
        #print(f'{indicator}={target} joltages={joltages} buttons={buttons} buttons_bin={button_values}')

        # Switch on: Indicator toggling
        p1_result += min_xor_presses(button_values, indicator_target)

        # Set Joltage: Joltage adding
        p2_result += min_add_presses(buttons, joltages)

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
