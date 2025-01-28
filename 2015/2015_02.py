#!python3
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '02',
    'url'           :   'https://adventofcode.com/2015/day/2',
    'name'          :   'I Was Told There Would Be No Math - Parcel wrapping',
    'difficulty'    :   'D1',
    'learned'       :   'Python list functions',
    't_used'        :   '20',
    'result_p1'     :   1586300,
    'result_p2'     :   3737498,
}
#############
TESTS = [
    {
        'name'  : 'Present-1',
        'input' : '2x3x4',
        'p1' : 58,
        'p2' : 34,
    },
    {
        'name'  : 'Present-2',
        'input' : '1x1x10',
        'p1' : 43,
        'p2' : 14,
    },
    {
        'name'  : 'Combined ',
        'input' : 
'''
2x3x4
1x1x10
''',
        'p1' : 101,
        'p2' : 48,
    },
]

#############
def solve(aoc_input, part1=True, part2=True, attr=None) :
    total_area, total_ribbon = 0, 0
    for present in aoc_input.splitlines() :
        if present == '' :
            continue
        l, w, h = sorted(list(map(int, present.split('x'))))
        a1 = l * w
        a2 = w * h
        a3 = h * l
        total_area += 2*(a1+a2+a3) + min(a1, a2, a3)
        total_ribbon += 2*(l+w) + l*w*h
    return total_area, total_ribbon

#############

if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
