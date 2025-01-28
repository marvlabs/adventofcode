#!python3
'''AoC 2024 Day 01'''
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '01',
    'url'           :   'https://adventofcode.com/2024/day/01',
    'name'          :   "Historian Hysteria: zip this list",
    'difficulty'    :   'D1',
    'learned'       :   'list functions',
    't_used'        :   '10',
    'result_p1'     :   1222801,
    'result_p2'     :   22545250,
}
#############
TESTS = [
{
'name'  : 'Location List',
'input' : '''3   4
4   3
2   5
1   3
3   9
3   3''',
'p1' : 11,
'p2' : 31,
},
]
#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    l1, l2 = [], []
    for string in aoc_input.splitlines()  :
        v1, v2 = string.split()
        l1.append(int(v1))
        l2.append(int(v2))

    p1_result = sum(abs(a-b) for a,b in zip (sorted(l1), sorted(l2)))
    p2_result = sum(a * l2.count(a) for a in l1)

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
