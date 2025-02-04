#!python3
'''AoC 2016 Day 10'''
import re
from math import prod
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '10',
    'url'           :   'https://adventofcode.com/2016/day/10',
    'name'          :   "Balance Bots - don't bogart them chips",
    'difficulty'    :   'D2',
    'learned'       :   'Don''t break too early',
    't_used'        :   '45',
    'result_p1'     :   'bot 118', 
    'result_p2'     :   143153,
}
#############
TESTS = [
{
    'name'  : 'pass-chips',
    'input' : '''value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2''',
    'p1' : 'bot 2',
    'p2' : None,
    'testattr'      :   (5,2)
},
]

#################

def pass_on(bots, rules, wanted_p1) :
    finished = False
    bot_found = None

    while not finished :
        finished = True
        
        for bot, vals in bots.items() :
            if len(vals) == 2 :
                # A bot has two items...
                if wanted_p1[0] in vals and wanted_p1[1] in vals :
                    # ... we're interested in
                    bot_found = bot
                
                if bot in rules :
                    # ... and a rule to pass them on
                    bots.setdefault(rules[bot][0], []).append(min(vals))
                    bots.setdefault(rules[bot][1], []).append(max(vals))
                    bots[bot].clear()
                    finished = False
                    break # Do another round - inventory has changed

    return bot_found


def solve(aoc_input, part1=True, part2=True, attr=None) :
    bots = {}
    rules = {}

    for line in aoc_input.splitlines() :
        if line.startswith('value') :
            values = re.findall(r'\d+', line)
            chip = int (values[0])
            bot = f'bot {values[1]}'
            bots.setdefault(bot, []).append(chip)
        elif line.startswith('bot') :
            bot, low, high = re.findall(r'(\w+? \d+)', line)
            rules[bot] = (low, high)
    
    # It doesn't matter whether we play through after every line, or only once after all chips have been doled out
    p1_result = pass_on(bots, rules, wanted_p1 = attr if attr else (61,17)) # attr for test case input
    p2_result = prod( [ bots[f'output {i}'][0] for i in range(3) ] ) if part2 else 0

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
