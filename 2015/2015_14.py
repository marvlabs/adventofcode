#!python3
'''AoC 2015 Day 14'''
import re
from collections import Counter
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '14',
    'url'           :   'https://adventofcode.com/2015/day/14',
    'name'          :   "Reindeer Olympics - Stutter Race",
    'difficulty'    :   'D2',
    'learned'       :   'Python regex groupdict, comprehensions again, Counter',
    't_used'        :   '60',
    'result_p1'     :   2696,
    'result_p2'     :   1084,
}
#############
TESTS = [
 {
        'name'  : 'Race-1',
        'input' : '''
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds
''',
        'p1' : 2660, #1120, # at 1000s
        'p2' : 1564, #689, # at 1000s
    },
]
#################
def calculate_distance(deer, time) :
    '''Stutter-math to calculate where a reindeer is at a given time. Use int/modulo/rest with period-length to check its state'''
    #period = deer['t_fly'] + deer['t_rest']
    return (time // deer['t_period']) * (deer['t_fly']*deer['v']) + min(time%deer['t_period'], deer['t_fly']) * deer['v']


def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    reindeer = {}
    for string in aoc_input.splitlines()  :
        if string == '' : continue
        #deer = re.match('(?P<name>.*) can fly (?P<v>\d+) km/s for (?P<t>\d+) seconds, but then must rest for (?P<rest>\d+)', string).groupdict()
        name, v, t_fly, t_rest = re.match('(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+)', string).groups()
        reindeer[name] = {'v': int(v), 't_fly': int(t_fly), 't_rest': int(t_rest), 't_period': int(t_fly)+int(t_rest)}

    p1_result = max(calculate_distance(deer, 2503) for deer in reindeer.values())

    score = Counter()
    for t_fly in range (1, 2504) :
        name_dist = [ (name, calculate_distance(deer, t_fly)) for name, deer in reindeer.items() ]
        maxdist = max(name_dist, key = lambda nd : nd[1])[1]
        score.update([ nd[0] for nd in name_dist if nd[1] == maxdist ]) # Multiple reindeer get a point if ahead abreast
    p2_result = score.most_common(1)[0][1]

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
