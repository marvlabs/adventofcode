#!python3
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '01',
    'url'           :   'https://adventofcode.com/2015/day/1',
    'name'          :   'Not Quite Lisp - Count braces',
    'difficulty'    :   'D1',
    'learned'       :   'My first Python program',
    't_used'        :   '20',
    'result_p1'     :   138,
    'result_p2'     :   1771,
}
#############
TESTS = [
    {
        'name'  : 'T1a',
        'input' : '(())',
        'p1' : 0,
        'p2' : None,
    },
    {
        'name'  : 'T1b',
        'input' : '()()',
        'p1' : 0,
        'p2' : None,
    },
    {
        'name'  : 'T2a',
        'input' : '(((',
        'p1' : 3,
        'p2' : None,
    },
    {
        'name'  : 'T2b',
        'input' : '(()(()(',
        'p1' : 3,
        'p2' : None,
    },
    {
        'name'  : 'T3 ',
        'input' : '))(((((',
        'p1' : 3,
        'p2' : None,
    },
    {
        'name'  : 'T4a',
        'input' : '())',
        'p1' : -1,
        'p2' : None,
    },
    {
        'name'  : 'T4b',
        'input' : '))(',
        'p1' : -1,
        'p2' : None,
    },
    {
        'name'  : 'T5a',
        'input' : ')))',
        'p1' : -3,
        'p2' : None,
    },
    {
        'name'  : 'T5b',
        'input' : ')())())',
        'p1' : -3,
        'p2' : None,
    },
    {
        'name'  : 'T6 ',
        'input' : ')',
        'p1' : -1,
        'p2' : 1,
    },
    {
        'name'  : 'T7 ',
        'input' : '()())',
        'p1' : -1,
        'p2' : 5,
    },]

#############
def solve(aoc_input, part1=True, part2=True, attr=None) :
    level = 0
    charpos_for_basement = None
    charpos = 0
    for brace in aoc_input:
        charpos += 1
        if brace == '(':
            level += 1
        elif brace == ')':
            level -= 1
        else:
            raise ValueError(f'Illegal char in input at pos {charpos} "{brace}"')

        if charpos_for_basement is None and level == -1 :
            charpos_for_basement = charpos

    return level, charpos_for_basement

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
