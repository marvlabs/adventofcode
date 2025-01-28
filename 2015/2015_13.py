#!python3
'''AoC 2015 Day 13'''
# from pprint import pprint as pp
import re
from itertools import permutations
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '13',
    'url'           :   'https://adventofcode.com/2015/day/13',
    'name'          :   "Knights of the Dinner Table - Happiness optimizer",
    'difficulty'    :   'D2',
    'learned'       :   'Python maps, generators and zip',
    't_used'        :   '45',
    'result_p1'     :   664,
    'result_p2'     :   640,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.''',
        'p1' : 330,
        'p2' : None,
    },
]
#################
def max_happiness(guestlist) :
    '''Make all possible circles from the guests using one guest to start and end, and permuting the in-betweens.
    (Could be optimized: this list duplicates for both circle directions)
    Return: Sum up all neighbors' happiness for each possible circle and return the max'''
    guest_names = list(guestlist.keys())
    circles = ([guest_names[0]] + list(p) + [guest_names[0]] for p in permutations(guest_names[1:]))
    happiness = lambda circle : sum(guestlist[name1][name2] + guestlist[name2][name1] for name1, name2 in zip(circle, circle[1:])) 
    return max(map(happiness, circles))


def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    guestlist = {}
    for string in aoc_input.splitlines()  :
        if string == '' : continue
        name1, lose_gain, happy, name2 = re.match(r'(.*) would (.*) (\d+) happiness units by sitting next to (.*)\.', string).groups()
        guestlist.setdefault(name1, {})[name2] = int(happy) * (1 if lose_gain == 'gain' else -1)
    p1_result = max_happiness(guestlist)
    
    # add me
    guest_names = guestlist.keys()
    guestlist['me'] = {}
    for guest in  guest_names:
        guestlist['me'][guest] = 0        
        guestlist[guest]['me'] = 0
    p2_result = max_happiness(guestlist)

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
