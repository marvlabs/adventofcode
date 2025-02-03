#!python3
'''AoC 2016 Day 06'''
from collections import Counter
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '06',
    'url'           :   'https://adventofcode.com/2016/day/06',
    'name'          :   "Signals and Noise - de-noised message",
    'difficulty'    :   'D1',
    'learned'       :   'zip again',
    't_used'        :   '5',
    'result_p1'     :   'xhnqpqql', 
    'result_p2'     :   'brhailro',
}
#############
TESTS = [
{
        'name'  : 'easter',
        'input' : '''eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar''',
        'p1' : 'easter',
        'p2' : 'advent',
},
]

#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = ''
    lines = aoc_input.splitlines()

    for column in zip(*lines) :
        count = Counter(column)
        p1_result += count.most_common(1)[0][0]
        p2_result += count.most_common()[-1][0]

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
