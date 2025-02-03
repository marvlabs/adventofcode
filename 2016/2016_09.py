#!python3
'''AoC 2016 Day 09'''
import re
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '09',
    'url'           :   'https://adventofcode.com/2016/day/09',
    'name'          :   "Explosives in Cyberspace - why use zip...",
    'difficulty'    :   'D2',
    'learned'       :   'Recurse is always easiset (ohhhh boy)',
    't_used'        :   '45',
    'result_p1'     :   74532, 
    'result_p2'     :   11558231665,
}
#############
TESTS = [
{
        'name'  : 'exp',
        'input' : '''ADVENT
A(1x5)BC
(3x3)XYZ
A(2x2)BCD(2x2)EFG
(6x1)(1x3)A
X(8x2)(3x3)ABCY''',
        'p1' : 6+7+9+11+6+18,
        'p2' : None,
},
{
        'name'  : 'exp(exp)',
        'input' : '''(3x3)XYZ
X(8x2)(3x3)ABCY
(27x12)(20x12)(13x14)(7x10)(1x12)A
(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN''',
        'p1' : None,
        'p2' : 9 + 20 + 241920 + 445,
},]
#################
marker_regex = re.compile("\((\d+)x(\d+)\)")

def decompress_1(input):
    text_len = 0
    repeat_end = 0
    for marker in marker_regex.finditer(input) :
        if marker.start() < repeat_end: continue # this marker is part of the last pattern
        num_chars, repeat = map(int, marker.groups())
        text_len += marker.start() - repeat_end + num_chars * repeat
        repeat_end = marker.end() + num_chars
    text_len += len(input) - repeat_end
    return text_len

def decompress_2(input):
    text_len = 0
    while m := marker_regex.search(input) :
        num_chars, repeat = map(int, m.groups())
        text_len += m.start() + decompress_2(input[m.end():m.end()+num_chars]) * repeat
        input = input[m.end()+num_chars:]
    return text_len + len(input)

def solve(aoc_input, part1=True, part2=True, attr=None) :
    input = ''.join(aoc_input.splitlines())
    p1_result = decompress_1(input)
    p2_result = decompress_2(input)
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    assert decompress_1("ADVENT") == 6
    assert decompress_1("A(1x5)BC") == 7
    assert decompress_1("(3x3)XYZ") == 9
    assert decompress_1("A(2x2)BCD(2x2)EFG") == 11
    assert decompress_1("(6x1)(1x3)A") == 6
    assert decompress_1("X(8x2)(3x3)ABCY") == 18

    assert decompress_2("(3x3)XYZ") == 9
    assert decompress_2("X(8x2)(3x3)ABCY") == 20
    assert decompress_2("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920
    assert decompress_2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
