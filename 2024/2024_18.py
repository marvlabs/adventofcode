#!python3
'''AoC 2024 Day 18'''
from grid import Grid, step
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '18',
    'url'           :   'https://adventofcode.com/2024/day/18',
    'name'          :   "RAM Run: leg it over",
    'difficulty'    :   'D2',
    'learned'       :   'A good think in the beginning helps',
    't_used'        :   '30',
    'result_p1'     :   252,
    'result_p2'     :   '5,60',
}
#############
TESTS = [
 {
'name'  : 'Small-Ram',
'input' : '''5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0''',
'testattr' : { 'side': 7, 'sim_steps': 12 }, # test restrictions
'p1' : 22,
'p2' : '6,1',
},
]
#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    falling = [ (int(x), int(y)) for x,y in [ string.split(',') for string in  aoc_input.splitlines() ] ]
    dim = 71           if not attr else attr['side']
    sim_steps = 1024   if not attr else attr['sim_steps']

    p1_result = len(run_maze(falling, dim, sim_steps)) -1

    # Binary search for how much ram to drop until the way is blocked
    bottom = sim_steps
    top = min(dim**2-2*dim, len(falling))
    while top - bottom > 1 :
        mid = (top + bottom) // 2
        if run_maze(falling, dim, mid) :
            bottom = mid
        else :
            top = mid
    p2_result = ','.join(map(str, falling[bottom]))

    return p1_result, p2_result


def run_maze(falling, dim, sim_steps) :
    ram = Grid(dim, dim, '.')

    # Drop some ram:
    for i in range(sim_steps) :
        ram.set(falling[i], '#')

    return find_path(ram, (0,0), (ram.dim_x-1, ram.dim_y-1))


# Visit all possible ajacent fields in a round. Stop when we see the end.
# Store where we come from to construct the path. Not strictly necessary, the cost would have been enough
def find_path(ram, pos_start, pos_end) :
    visited = {}
    reachable = { pos_start : None }

    while len (reachable) > 0 :
        next_positions = {}
        for pos, come_from in reachable.items() :
            for dir, field in ram.neighbours90(pos).items() :
                if field and field != '#' :
                    pos_next = step(pos, dir)
                    if pos_next not in visited and pos_next not in reachable :
                        next_positions[pos_next] = pos
            visited[pos] = come_from
        reachable = next_positions

        if pos_end in reachable :
            path = [ pos_end ]
            next = reachable[pos_end]
            while next != pos_start :
                path.append(next)
                next = visited[next]
            path.append(pos_start)
            path.reverse()
            return path
    
    return None

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
