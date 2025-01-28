#!python3
'''AoC 2024 Day 23'''
from itertools import permutations
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '23',
    'url'           :   'https://adventofcode.com/2024/day/23',
    'name'          :   "LAN Party: Connect them computers",
    'difficulty'    :   'D2',
    'learned'       :   'Sets iterations - maybe check some algos?',
    't_used'        :   '30',
    'result_p1'     :   1370,
    'result_p2'     :   'am,au,be,cm,fo,ha,hh,im,nt,os,qz,rr,so',
}
#############
TESTS = [
{
    'name'  : 'SmallLan',
    'input' : '''kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn''',
    'p1' : 7,
    'p2' : 'co,de,ka,ta',
},
]
#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    connections = {}
    for string in aoc_input.splitlines()  :
        c1, c2 = string.split('-')
        connections[c1] = connections.get(c1, []) + [c2]
        connections[c2] = connections.get(c2, []) + [c1]

    # Part one - find all three-groups
    threes = set()
    threes_t = set()
    for c1 in connections :
        for c2, c3 in permutations(connections[c1], 2) :
            if c2 in connections[c3] :
                three = tuple(sorted([c1, c2, c3]))
                threes.add(three)
                if 't' in (c1 + c2 + c3)[::2]:
                    threes_t.add(three)

    # Expand all three-groups to their max: try to add every other computer. It must connect to all others in the group
    # Not very efficient maybe...
    max_group = set()
    for three in threes :
        group = set(three)
        for c_new in connections :
            if c_new in group : continue
            c_to_group = True
            for c in group :
                if c_new not in connections[c] : 
                    c_to_group = False
                    break
            if c_to_group : group.add(c_new)
        if len(group) > len(max_group) :
            max_group = group


    p1_result = len(threes_t)
    p2_result = ','.join(map(str, sorted(max_group)))

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
