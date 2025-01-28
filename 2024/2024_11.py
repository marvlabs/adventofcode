#!python3
'''AoC 2024 Day 11'''
# from pprint import pprint as pp
import functools

#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '11',
    'url'           :   'https://adventofcode.com/2024/day/11',
    'name'          :   "Plutonian Pebbles: Don't Blink, Doctor!",
    'difficulty'    :   'D2',
    'learned'       :   'memoizated recursion, again',
    't_used'        :   '15',
    'result_p1'     :   185205,
    'result_p2'     :   221280540398419,
}
#############
TESTS = [
 {
        'name'  : 'Pluto-1',
        'input' : '''125 17''',
        'p1' : 55312,
        'p2' : None,
    },
]
#################

# Memoize that: Without, this would take some three years...
@functools.cache
def pluto(nr, currdepth) :
    if currdepth == 0 :
        return 1

    if nr == 0 :
        return pluto(1, currdepth-1)
    elif (l := len(str(nr))) % 2 == 0 :
        return pluto(int(str(nr)[:l//2]), currdepth-1) + pluto(int(str(nr)[l//2:]), currdepth-1)
    else:
        return pluto(nr*2024, currdepth-1)


# Trying my own cache instead of functools:
# It's a tiny bit more memory efficient, because it does not need to cache the last call
# It's not faster - surprising considering that it's a non-general implementation.
# Turns out that functools has a C implementation, while mine must use key/dict from Python
#key = lambda nr, blinks_left : f'{nr}_{blinks_left}' # '123_12'
#key = lambda nr, blinks_left : nr+blinks_left/100    #  123.12 f -> it's a bit faster
key = lambda nr, blinks_left : nr*100+blinks_left    #  12312 -> even faster
cache = {}
def my_pluto(nr, blinks_left) :
    if blinks_left == 0 :
        return 1

    k = key(nr, blinks_left)
    if k in cache:
       return cache[k] 
    
    if nr == 0 :
        stones = my_pluto(1, blinks_left-1)
    elif (l := len(str(nr))) % 2 == 0 :
        stones = my_pluto(int(str(nr)[:l//2]), blinks_left-1) + my_pluto(int(str(nr)[l//2:]), blinks_left-1)
    else :
        stones = my_pluto(nr*2024, blinks_left-1)

    cache[k] = stones
    return stones


USE_MY_CACHE=1
def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0
    for nr in map(int, aoc_input.split())  :
        p1_result += USE_MY_CACHE and my_pluto(nr, 25) or pluto(nr, 25)
        p2_result += USE_MY_CACHE and my_pluto(nr, 75) or pluto(nr, 75)
    print ("   -> cache size: ", len(cache) if USE_MY_CACHE else pluto.cache_info())
    return p1_result, p2_result


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
