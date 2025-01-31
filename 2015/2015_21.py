#!python3
'''AoC 2015 Day xx'''
# from pprint import pprint as pp
import re
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '21',
    'url'           :   'https://adventofcode.com/2015/day/21',
    'name'          :   "sRPG Simulator 20XX",
    'difficulty'    :   'D2',
    'learned'       :   'Some parsing and combination stuff',
    't_used'        :   '45',
    'result_p1'     :   91,
    'result_p2'     :   158,
}
#############
TESTS = []
#################
Inventory_list = '''
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
NoArmor      0      0       0
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
NoRing1     0     0       0
NoRing2     0     0       0
Damage1    25     1       0
Damage2    50     2       0
Damage3   100     3       0
Defense1   20     0       1
Defense2   40     0       2
Defense3   80     0       3
'''


def parse_inventory(string) :
    inventory = {
    'Weapons' : {},
    'Armor' : {},
    'Rings' : {},
}
    cat = ''
    for s in string.splitlines() :
        if s == '' : 
            continue
        elif (p := s.find(':')) > 0 :
            cat = s[:p]
        else:
            (name, cost, damage, armor) = s.split()
            inventory[cat][name] = {'cost' : int(cost), 'damage' : int(damage), 'armor' : int(armor)}
    return inventory

def all_outfits(inventory) :
    for w, wi in inventory['Weapons'].items() :
        for a, ai in inventory['Armor'].items() :
            for r1, r1i in inventory['Rings'].items() :
                if r1 == 'NoRing2' : continue
                for r2, r2i in inventory['Rings'].items() :
                    if r2 == 'NoRing1': continue
                    yield { 
                            'name' : f'{w}-{a}-{r1}-{r2}',
                            'Hit Points' : 100,
                            'cost' : wi['cost'] + ai['cost'] + r1i['cost'] + r2i['cost'],
                            'Damage' : wi['damage'] + ai['damage'] + r1i['damage'] + r2i['damage'],
                            'Armor' : wi['armor'] + ai['armor'] + r1i['armor'] + r2i['armor'],
                    }


def win_fight(me, boss) :
    points_me = me['Hit Points']
    points_boss = boss['Hit Points']
    while True :
        # Player
        points_boss -= max(me['Damage'] - boss['Armor'], 1)
        if points_boss <= 0 :
            return True
        # Boss
        points_me -= max(boss['Damage'] - me['Armor'], 1)
        if points_me <= 0 :
            return False


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0

    boss = { 'name': 'BOSS'}
    for string in aoc_input.splitlines()  :
        id, val = string.split(': ')
        boss[id] = int(val)

    inventory = parse_inventory(Inventory_list)

    for outfit in sorted(all_outfits(inventory), key=lambda x: x['cost']) :
        if win_fight(outfit, boss) :
            print (f"I WON with {outfit['name']} at cost {outfit['cost']}")
            p1_result = outfit['cost']
            break

    for outfit in sorted(all_outfits(inventory), key=lambda x: x['cost'], reverse=True) :
        if not win_fight(outfit, boss) :
            print (f"I LOST with {outfit['name']} at cost {outfit['cost']}")
            p2_result = outfit['cost']
            break

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
