#!python3
'''AoC 2015 Day xx'''
from math import sqrt
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '20',
    'url'           :   'https://adventofcode.com/2015/day/20',
    'name'          :   "Infinite Elves and Infinite Houses",
    'difficulty'    :   'D2',
    'learned'       :   'Run the elves, not the houses - Presis for all!',
    't_used'        :   '30',
    'result_p1'     :   831600,
    'result_p2'     :   884520,
}
#############
TESTS = [
 {
        'name'  : 't-9',
        'input' : '130',
        'p1' : 60,
        'p2' : 20,
    },
]
#################

def do_elf(elf, houses, target, limit=0, factor=10) :
    house_nr = elf
    for i in range(1, len(houses)) :
        if limit > 0 and i > limit :
            return 0
        if house_nr >= len(houses) :
            return 0
        
        houses[house_nr] += factor*elf
        
        if houses[house_nr] >= target :
            #print (house_nr, houses[house_nr])
            return house_nr
        
        house_nr += elf

    return 0

def find_house(target, factor, limit) :
    nr_of_houses = int(1E6) # should be enough? If no result, increase
    houses = [ factor ] * nr_of_houses # start with elf 2, prepopulate elf one visits

    for elf in range(2, nr_of_houses+1) : 
        res = do_elf(elf, houses, target, limit, factor)
        if res > 0 :
            return res
    return 0

def solve(aoc_input, part1=True, part2=True, attr=None) :
    target = int(aoc_input)

    p1_result = find_house(target, 10, 0)
    p2_result = find_house(target, 11, 50)
    
    return p1_result, p2_result


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
