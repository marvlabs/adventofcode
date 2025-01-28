#!python3
'''AoC 2015 Day 15'''
# from pprint import pprint as pp
import re
from functools import reduce
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '15',
    'url'           :   'https://adventofcode.com/2015/day/15',
    'name'          :   "Science for Hungry People - Cookie Recipe",
    'difficulty'    :   'D2',
    'learned'       :   'Python yield generator function, reduce',
    't_used'        :   '90',
    'result_p1'     :   21367368,
    'result_p2'     :   1766400,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
''',
        'p1' : 62842880,
        'p2' : 57600000,
    },
]
#################
def combine_items_to_x(items, x) :
    '''Generator - yield all tuple combinations with items for x slots
    items: how many items to assign
    x: how many slots. > 0
    returns: Generator for all possible tuples, i.e. (2,3) -> (0, 3) (1, 2) (2, 1) (3, 0)'''
    if items == 1 :
        yield (x,)
        return
    for i, sub in ((i,sub) for i in range(x+1) for sub in combine_items_to_x(items-1, x-i)) :
        yield (i,) + sub
    return


def score_cookie(recipe, ingredients) :
    '''calculate the cookie score for the given ratio and the values in the ingredients.
    return: score and calories'''
    cookie = {}
    for attr in (key for key in ingredients[0].keys() if key != 'name') :
        cookie[attr] = sum(ingredients[i][attr] * recipe[i] for i in range(len(recipe)))
        if cookie[attr] <= 0 : 
            return 0, 0
    return (reduce(lambda x,y : x*y, ( item[1] for item in cookie.items() if item[0] != 'cal') ), cookie['cal'])


def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    ingredients = []
    for string in aoc_input.splitlines()  :
        if string == '' : continue
        name, capacity, durability, flavor, texture, calories = re.match(r'(.*): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)', string).groups()
        ingredients.append({'name': name, 'c': int(capacity), 'd': int(durability), 'f': int(flavor), 't': int(texture), 'cal': int(calories)})
    
    p1_result = max(score_cookie(recipe, ingredients)[0] for recipe in combine_items_to_x(len(ingredients), 100))
    p2_result = max(score[0] for score in ( score_cookie(recipe, ingredients) for recipe in combine_items_to_x(len(ingredients), 100) ) if score[1] == 500)

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
