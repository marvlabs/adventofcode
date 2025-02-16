#!python3
'''AoC 2016 Day 18'''
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '18',
    'url'           :   'https://adventofcode.com/2016/day/18',
    'name'          :   "Like a Rogue - finding the safe tiles",
    'difficulty'    :   'D2',
    'learned'       :   'Optimization not always necessary',
    't_used'        :   '15',
    'result_p1'     :   2016, 
    'result_p2'     :   19998750,
}
#############
TESTS = [
{
    'name'  : 'tiles-10',
    'input' : '''.^^.^.^^^^''',
    'p1' : 38,
    'p2' : None,
    'testattr' : 10
},
]

#################
traps = ['^^.', '.^^', '^..', '..^']
def next_row(row) :
    return ''.join( '^' if ('.' + row + '.')[i:i+3] in traps else '.' for i in range(len(row)) )
assert next_row('..^^.') == '.^^^^'
assert next_row('.^^^^') == '^^..^'

# P1 solution also works for part 2 with 400000 instead of 40 rows, takes 6s.
# Can we optimize by finding a pattern maybe? -> Would work on test input, but the real input has too many variations at 100 bit
def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = 0
    size_p1 = 40 if not attr else attr
    size_p2 = 400000 if not attr else attr
    
    row = aoc_input.strip()
    for i in range(size_p2) :
        if i < size_p1 : p1_result += row.count('.')
        p2_result += row.count('.')
        row = next_row(row)

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
