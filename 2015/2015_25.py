#!python3
'''AoC 2015 Day 25'''
import re
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '25',
    'url'           :   'https://adventofcode.com/2015/day/25',
    'name'          :   "Let It Snow - number finding",
    'difficulty'    :   'D2',
    'learned'       :   'Gauss\' sum formula',
    't_used'        :   '30',
    'result_p1'     :   9132360, 
    'result_p2'     :   None,
}
#############
TESTS = [
{
        'name'  : 'test_4_4',
        'input' : '''To continue, please consult the code grid in the manual.  Enter the code at row 4, column 4.''',
        'p1' : 9380097,
        'p2' : None,
},
{
        'name'  : 'test_6_5',
        'input' : '''To continue, please consult the code grid in the manual.  Enter the code at row 6, column 5.''',
        'p1' : 1534922,
        'p2' : None,
},]

#################

init_val = 20151125
mul_val  = 252533
div_val  = 33554393

# Gauss' sum formula to get the triangle top number needed (1 3 6 10 15 21...), then adjust the row down
def n_from_row_col(row, col) :
    top = col + row-1
    return (top * (top + 1) // 2) - (row-1)

def nth_value(n) :
    val = init_val
    for i in range(1, n) :
        val = (val * mul_val) % div_val
    return val

def solve(aoc_input, part1=True, part2=True, attr=None) :
    row, column =  re.findall(r'\d+', aoc_input)

    p1_result = nth_value(n_from_row_col(int(row), int(column)))
    return p1_result, None

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    assert n_from_row_col(1, 1) == 1
    assert n_from_row_col(2, 2) == 5
    assert n_from_row_col(1, 6) == 21
    assert n_from_row_col(5, 2) == 17
    assert nth_value(1) == 20151125
    assert nth_value(2) == 31916031
    assert nth_value(20) == 15514188

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
