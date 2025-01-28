#!python3
'''AoC 2015 Day 09'''
from itertools import permutations
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '09',
    'url'           :   'https://adventofcode.com/2015/day/9',
    'name'          :   "All in a Single Night - Brute Pathfinding",
    'difficulty'    :   'D2',
    'learned'       :   'Python dict, lists, recursion vs permutations',
    't_used'        :   '45',
    'result_p1'     :   207,
    'result_p2'     :   804,
}
#############
TESTS = [
 {
        'name'  : 'Cities',
        'input' : '''
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
''',
        'p1' : 605,
        'p2' : 982,
    },
]
#################
CITIES = None

# The permutation solution below is faster and much cleaner
# 70000 recusive calls used for the 8 cities
# def visit_cities_recurse(coming_from, already_travelled_shortest, already_travelled_longest, citylist) :
#     '''recusive: go to all cities from here, return shortest and longest possible paths'''
#     global DEBUG_CALLS; DEBUG_CALLS += 1
#     shortest = 1E9
#     longest = 0
#     for nextcity in citylist :
#         travelling_shortest = already_travelled_shortest + CITIES[coming_from][nextcity] if coming_from is not None else 0
#         travelling_longest  = already_travelled_longest  + CITIES[coming_from][nextcity] if coming_from is not None else 0
#         to_visit = [ c for c in citylist if c != nextcity ]
#         if len(to_visit) == 0 :
#             return travelling_shortest, travelling_longest
#         dist1, dist2 = visit_cities_recurse(nextcity, travelling_shortest, travelling_longest, to_visit)
#         shortest = min(shortest, dist1)
#         longest = max(longest, dist2)
#     return shortest, longest

def visit_cities_permute(citylist) :
    '''permuations: use lib for all possible combos, map-compute distances'''
    route_dist = lambda route : sum(map(lambda c1, c2 : CITIES[c1][c2], route, route[1:]))
    distances = list(map(route_dist, permutations(citylist)))
    return min(distances), max(distances)

def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    p1_result, p2_result = 0, 0
    global CITIES
    CITIES = {}
    for string in aoc_input.splitlines()  :
        if string == '' : continue
        c1, _, c2, _, dist = string.split()
        CITIES.setdefault(c1, {})[c2] = int(dist)
        CITIES.setdefault(c2, {})[c1] = int(dist)

    return visit_cities_permute(CITIES.keys())
    #return visit_cities_recurse(None, 0, 0, CITIES.keys())
#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
