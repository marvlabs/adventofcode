#!python3
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '03',
    'url'           :   'https://adventofcode.com/2015/day/3',
    'name'          :   'Perfectly Spherical Houses in a Vacuum - Santa steps',
    'difficulty'    :   'D1',
    'learned'       :   'Python Tuple, enumerate',
    't_used'        :   '30',
    'result_p1'     :   2081,
    'result_p2'     :   2341,
}
#############
TESTS = [
    {
        'name'  : 'House-1',
        'input' : '>',
        'p1' : 2,
        'p2' : None,
    },
    {
        'name'  : 'House-2',
        'input' : '^>v<',
        'p1' : 4,
        'p2' : 3,
    },
    {
        'name'  : 'House-3',
        'input' : '^v^v^v^v^v',
        'p1' : 2,
        'p2' : 11,
    },
    {
        'name'  : 'House-4',
        'input' : '^v',
        'p1' : None,
        'p2' : 3,
    },
]
#############
def go(dir) :
    return {
        '>' : (1,0),
        'v' : (0,1),
        '<' : (-1,0),
        '^' : (0,-1),
    } [dir]

def next(pos, dir) :
    return (pos[0] + go(dir)[0], pos[1] + go(dir)[1])

def key(pos) :
    return str(pos[0]) + '/' + str(pos[1])

#############
def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1 = solve_p1(aoc_input) if part1 else None
    p2 = solve_p2(aoc_input) if part2 else None
    return p1, p2


def solve_p1(aoc_input) :
    pos = (0,0)
    visited = { key(pos) : 1}
    for dir in aoc_input :
        pos = next(pos, dir)
        visited[key(pos)] = visited.get(key(pos), 0) + 1
        
    return len(visited)


def solve_p2(aoc_input) :
    pos_santa = (0,0)
    pos_robo = (0,0)
    visited = { key(pos_santa) : 1}
    visited = { key(pos_robo) : 1}
    for idx, dir in enumerate(aoc_input) :
        if idx%2 == 0 :
            pos_santa = next(pos_santa, dir)
            visited[key(pos_santa)] = visited.get(key(pos_santa), 0) + 1
        else:
            pos_robo = next(pos_robo, dir)
            visited[key(pos_robo)] = visited.get(key(pos_robo), 0) + 1
        
    return len(visited)

#############

if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
