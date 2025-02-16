#!python3
'''AoC 2016 Day 17'''
from hashlib import md5
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '17',
    'url'           :   'https://adventofcode.com/2016/day/17',
    'name'          :   "Two Steps Forward - MD5 door maze",
    'difficulty'    :   'D2',
    'learned'       :   'Take care in recursions',
    't_used'        :   '30',
    'result_p1'     :   'RLDUDRDDRR', 
    'result_p2'     :   590,
}
#############
TESTS = [
{
    'name'  : 'maze1',
    'input' : '''ihgpwlah''',
    'p1' : 'DDRRRD',
    'p2' : 370,
},
{
    'name'  : 'maze2',
    'input' : '''kglvqrro''',
    'p1' : 'DDUDRLRRUDRD',
    'p2' : 492,
},
{
    'name'  : 'maze3',
    'input' : '''ulqzkmiv''',
    'p1' : 'DRURDRUDDLLDLUURRDULRLDUUDDDRR',
    'p2' : 830,
},
]

#################
directions = {'U': (0,-1), 'D': (0,1), 'L': (-1,0), 'R': (1,0)}
start = (0,0)
end   = (3,3)
shortest = 100 # optimise : prune unnecessary paths

valid_pos = lambda pos : pos[0] >= 0 and pos[0] < 4 and pos[1] >= 0 and pos[1] < 4
def open_doors(seed, pos, path) :
    doors = []
    code = md5((seed+path).encode()).hexdigest()
    for i, d in enumerate('UDLR') :
        if code[i] in 'bcdef' :
            next_pos = (pos[0] + directions[d][0], pos[1] + directions[d][1])
            if not valid_pos(next_pos) : continue
            doors.append ((next_pos, path+d))
    return doors

def walk(seed, pos, next_path) :
    global shortest
    if len(next_path) >= shortest-1 : return None

    next_rooms = open_doors(seed, pos, next_path)

    # Optimise: don't walk any more - possibly very long - paths if we can reach the end
    for next_pos, next_path in next_rooms : 
        if next_pos == end : 
            shortest = len(next_path)
            return next_path

    results = []
    for next_pos, next_path in next_rooms :
        result = walk(seed, next_pos, next_path)
        if result : results.append(result)

    return min(results, key=len, default=None)


def walk_longest(seed, pos, path) :
    if pos == end : return path
    
    next_rooms = open_doors(seed, pos, path)

    results = []
    for next_pos, next_path in next_rooms :
        result = walk_longest(seed, next_pos, next_path)
        if result : results.append(result)

    return max(results, key=len, default=None)


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = 0
    seed = aoc_input.strip()

    global shortest
    shortest = 100
    p1_result = walk(seed, start, '')
    p2_result = len(walk_longest(seed, start, ''))

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
