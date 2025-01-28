#!python3
'''AoC 2024 Day 13'''
# from pprint import pprint as pp
import re
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '13',
    'url'           :   'https://adventofcode.com/2024/day/13',
    'name'          :   "Claw Contraption: smash those buttons",
    'difficulty'    :   'D2',
    'learned'       :   'Brush up on equations :)',
    't_used'        :   '45',
    'result_p1'     :   29388,
    'result_p2'     :   99548032866004,
}
#############
TESTS = [
 {
        'name'  : '4-Claws',
        'input' : '''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
''',
        'p1' : 480,
        'p2' : 875318608908,
    },
]

#################
def equation(Ax, Ay, Bx, By, Px, Py) :
    a = (Px*By - Py*Bx) / (Ax*By - Ay*Bx)
    #b = (Px*Ay - Py*Ax) / (Ay*Bx - Ax*By)
    b=(Py - a*Ay)/By
    return a, b

def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    p1_result, p2_result = 0, 0
    digits = [ list( map( int, re.findall( "-?\\d+", s ) ) ) for s in aoc_input.split( "\n\n" ) ]
    for Ax, Ay, Bx, By, Px, Py in digits :
            a, b = equation(Ax, Ay, Bx, By, Px, Py)
            if (int(a) == a and int(b) == b) :
                p1_result += a*3 + b

            a, b = equation(Ax, Ay, Bx, By, Px+10000000000000, Py+10000000000000)
            if (int(a) == a and int(b) == b) :
                p2_result += a*3 + b

            #print (Ax, Ay, Bx, By, Px, Py, a, b)

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
