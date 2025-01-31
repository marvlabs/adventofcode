#!python3
'''AoC 2015 Day xx'''
from copy import deepcopy
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '22',
    'url'           :   'https://adventofcode.com/2015/day/22',
    'name'          :   "Wizard Simulator 20XX - recurse fights",
    'difficulty'    :   'D2',
    'learned'       :   'Aaaarghh, ONE small mistake cost hours',
    't_used'        :   '180',
    'result_p1'     :   900,
    'result_p2'     :   1216,
}
#############
TESTS = []
#################
Spells = {
    'Missile' : { 'cost':  53, 'damage': 4, 'armor' : 0, 'heal': 0, 'turns': 1, 'mana':   0},
    'Drain'   : { 'cost':  73, 'damage': 2, 'armor' : 0, 'heal': 2, 'turns': 1, 'mana':   0},
    'Shield'  : { 'cost': 113, 'damage': 0, 'armor' : 7, 'heal': 0, 'turns': 6, 'mana':   0},
    'Poison'  : { 'cost': 173, 'damage': 3, 'armor' : 0, 'heal': 0, 'turns': 6, 'mana':   0},
    'Recharge': { 'cost': 229, 'damage': 0, 'armor' : 0, 'heal': 0, 'turns': 5, 'mana': 101},
}

MinMana = 2000 # prune expensive paths, arbitrary start limit to prevent defensive escalation in depth first search

def fight(me, boss, effects, is_my_turn, mana_spent, current_path, is_hard) :
    global MinMana

    if mana_spent >= MinMana : return -1

    if is_hard and is_my_turn :
        me['Hit Points'] -= 1
        if me['Hit Points'] <= 0 : return -1

    me['armor'] = 0
    for e in effects :
        if effects[e] > 0 :
            boss['Hit Points'] -= Spells[e]['damage']
            me['armor']        += Spells[e]['armor']
            me['Hit Points']   += Spells[e]['heal']
            me['mana']         += Spells[e]['mana']
            effects[e] -= 1

    if boss['Hit Points'] <= 0 :
        return mana_spent

    if is_my_turn :
        if me['mana'] < 53 : return -1 # no mana left for cheapest spell

        # Try all spells available recursively
        results = []
        for spell_name, spell in Spells.items() :
            if me['mana'] < spell['cost'] : continue # Can't afford it
            if effects[spell_name] > 0    : continue # Already active

            # Try spell
            next_me = deepcopy(me)
            next_boss = deepcopy(boss)
            next_effects = deepcopy(effects)
            next_me['mana'] -= spell['cost'] 
            next_effects[spell_name] = spell['turns']
            res = fight(next_me, next_boss, next_effects, False, mana_spent + spell['cost'], current_path + spell_name + ' ', is_hard)
            if res > 0 : results.append(res)
        
        if len(results) == 0 : return -1 # No way to win cheaper found

        if min(results) < MinMana :      # Found a new minimum path
            MinMana = min(results)
            print(f'New Minimum: {MinMana} with fight {current_path}')

        return min(results)
    
    else :
        # Boss turn
        me['Hit Points'] -= max(boss['Damage'] - me['armor'], 1)
        if me['Hit Points'] <= 0 : return -1 # Dead
        return fight(me, boss, effects, True, mana_spent, current_path, is_hard) # Next me turn


def solve(aoc_input, part1=True, part2=True, attr=None) :
    global MinMana # to be able to reset for p2...

    effects = { 'Missile': 0, 'Drain': 0, 'Shield': 0, 'Poison': 0, 'Recharge' : 0 }
    me = { 'mana': 500, 'armor' : 0, 'Hit Points': 50 }
    boss = { 'name': 'BOSS'}
    for string in aoc_input.splitlines()  :
        id, val = string.split(': ')
        boss[id] = int(val)

    p1_result = fight(deepcopy(me), deepcopy(boss), deepcopy(effects), True, 0, 'PATH: ', is_hard=False)
    MinMana = 2000
    p2_result = fight(me, boss, effects, True, 0, 'PATH: ', is_hard=True)

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
