#!python3
'''AoC 2015 Day 08'''
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '08',
    'url'           :   'https://adventofcode.com/2015/day/8',
    'name'          :   "Matchsticks - Esc Me",
    'difficulty'    :   'D1',
    'learned'       :   'Translate',
    't_used'        :   '20',
    'result_p1'     :   1333,
    'result_p2'     :   2046,
}
#############
TESTS = [
 {
        'name'  : 'Esc-1',
        'input' : '''
""
"abc"
"aaa\\"aaa"
"\\x27"
''',
        'p1' : 12,
        'p2' : 19,
    },
]
#################
def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    p1_result, p2_result = 0, 0
    esc_translate = str.maketrans({'"' : '\\"', '\\' : '\\\\'})

    for string in aoc_input.splitlines()  :
        if string == '' : continue
        len_code = len(string)
        len_literal = len(bytes(string, "utf-8").decode("unicode_escape"))
        len_expanded = len(string.translate(esc_translate))
        p1_result += len_code - len_literal + 2
        p2_result += len_expanded - len_code + 2

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    assert bytes("aaa\"aaa", "utf-8").decode("unicode_escape") == 'aaa"aaa'
    assert bytes("\x32", "utf-8").decode("unicode_escape") == '2'

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
