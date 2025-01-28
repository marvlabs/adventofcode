#!python3
'''AoC 2015 Day 12'''
import re
import json
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '12',
    'url'           :   'https://adventofcode.com/2015/day/12',
    'name'          :   "JSAbacusFramework.io - JSON sum",
    'difficulty'    :   'D1',
    'learned'       :   'regex, JSON',
    't_used'        :   '30',
    'result_p1'     :   191164,
    'result_p2'     :   87842,
}
#############
TESTS = [
    {
        'name'  : 'test',
        'input' : '''[[1,2,3],{"a":2,"b":4},[[[3]]],{"a":{"b":4},"c":-1},[],{}]''',
        'p1' : 18,
        'p2' : 18,
    },
    {
        'name'  : 'test',
        'input' : '''[[1,2,3], [1,{"c":"red","b":2},3], {"d":"red","e":[1,2,3,4],"f":5}, [1,"red",5] ]''',
        'p1' : 33,
        'p2' : 16,
    },
]
#################

def sum_wo_red(item) :
    '''check item: return value if int, recurse sum if list or dict value - unless a dict value is "red"'''
    if isinstance(item, int) :
        return item
    elif isinstance(item, list) :
        return sum([ sum_wo_red(i) for i in item ])
    elif isinstance(item, dict) and 'red' not in item.values() : 
        return sum([ sum_wo_red(i) for i in item.values() ])
    return 0


def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    p1_result = sum(map(int, re.findall(r'-?\d+', aoc_input)))
    p2_result = sum_wo_red(json.loads(aoc_input))
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
