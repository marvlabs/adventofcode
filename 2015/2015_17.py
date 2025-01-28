#!python3
'''AoC 2015 Day 17'''
# from pprint import pprint as pp
import re
from itertools import product
from collections import Counter 

#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '17',
    'url'           :   'https://adventofcode.com/2015/day/17',
    'name'          :   "No Such Thing as Too Much - Fill them containers",
    'difficulty'    :   'D2',
    'learned'       :   'Permutations, lists, Counter',
    't_used'        :   '60',
    'result_p1'     :   4372,
    'result_p2'     :   4,
}
#############
TESTS = [
    {
        'name'  : 'Eggnogg-1',
        'input' : '''
20
15
10
5
5
''',
        'p1' :4, # for 25l
        'p2' :3, # for 25l
        'testattr': 25
    },
]
#################


def nr_of_combinations(containers, target_volume) :
    '''Each container can be used or not -> represented by all permutations of a bit-list the length of the containers list.
    zip-product of bits with containers summed up and checked against the target volume -> valid combination.
    Count the on bits into a counter, then return the sum and the number in the entry with the lowest bit count'''
    permutations =  product([0,1], repeat=len(containers))
    solution_container_count = Counter(sum(perm) for perm in permutations if sum(x*y for x,y in zip(containers, perm)) == target_volume)
    return sum(solution_container_count.values()) , min(solution_container_count.items(), key=lambda x: x[0])[1]


def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    volume = 150 if not attr else attr
    containers =  [ int(container.strip()) for container in aoc_input.splitlines() if container ]
    p1_result, p2_result = nr_of_combinations(containers, volume)
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)


# First solution: It makes an actual list of all possible container combinations, then sums and filters.
# But actually, we only need the combinations which work in a list, and not the containers with volumes -> see below
# def nr_of_combinations(containers, target_volume) :
#     permutations = product([0,1], repeat=len(containers))
#     containers_filled = ( [x*y for x,y in zip(containers, perm)] for perm in permutations )
#     filled_volumes = ( sum(prod) for prod in containers_filled )
#     return sum(filled == target_volume for filled in filled_volumes)
# def nr_of_min_combinations(containers, target_volume) :
#     permutations = product([0,1], repeat=len(containers))
#     containers_filled = [ [x*y for x,y in zip(containers, perm)] for perm in permutations  ]
#     filled_volumes = [ sum (prod) for prod in containers_filled ]
#     count = 0
#     min_container = len(containers)
#     for i, s in enumerate(filled_volumes) :
#         if s != target_volume : continue
#         nr_of_containers = len(containers_filled[i]) - containers_filled[i].count(0)
#         if nr_of_containers < min_container :
#             min_container = nr_of_containers
#             count = 1
#         elif nr_of_containers ==  min_container :
#             count += 1
#     return count