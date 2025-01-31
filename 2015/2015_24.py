#!python3
'''AoC 2015 Day 24'''
from itertools import combinations
from functools import reduce
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '24',
    'url'           :   'https://adventofcode.com/2015/day/24',
    'name'          :   "It Hangs in the Balance - group the Presis",
    'difficulty'    :   'D2',
    'learned'       :   'Combination shortcuts',
    't_used'        :   '60',
    'result_p1'     :   10723906903, 
    'result_p2'     :   74850409,
}
#############
TESTS = [
{
        'name'  : '1-11',
        'input' : '''1
2
3
4
5
7
8
9
10
11''',
        'p1' : 99,
        'p2' : 44,
},
]

#################
# We look for small, heavy groups of packages that sum to 1/3 and 1/4 of the total weight, enlarging the group size until we find at least one combination.
# ...coldly assuming that the remaining packages can be grouped into two equal loads...
def find_small_group(pakets, weight) :
    groups = []
    pakets_heavy = sorted(pakets, reverse=True)
    for nr_of_elems in range(2, len(pakets_heavy)//4+1) :
        for group in combinations(pakets_heavy, nr_of_elems) :
            if sum(group) == weight :
                groups.append(list(group))
        if len(groups) > 0 : break
    return groups


def solve(aoc_input, part1=True, part2=True, attr=None) :
    pakets =  [ int(i) for i in aoc_input.split('\n') if i != '' ]

    total_weight = sum(pakets)
    group_list = find_small_group(pakets, total_weight // 3)
    quantums = [ reduce(lambda a,b : a*b, l) for l in group_list ]
    p1_result = min(quantums)

    group_list = find_small_group(pakets, total_weight // 4)
    quantums = [ reduce(lambda a,b : a*b, l) for l in group_list ]
    p2_result = min(quantums)

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
