#!python3
'''AoC 2024 Day 16'''
from grid import Grid, step
import sys
#############
# DEPRECATED. This works, but it takes more than two minutes.
# The Dijkstra is SO MUCH FASTER at 60ms ...
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '16',
    'url'           :   'https://adventofcode.com/2024/day/16',
    'name'          :   "Reindeer Maze: lots of ways",
    'difficulty'    :   'D3',
    'learned'       :   'Patience in recursion (DEPRECATED. The Dijkstra is SO MUCH FASTER)',
    't_used'        :   '90',
    'result_p1'     :   82460,
    'result_p2'     :   590,
}
#############
TESTS = [
{
'name'  : 'Maze1',
'input' : '''
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
''',
'p1' : 7036,
'p2' : 45,
},
{
'name'  : 'Maze2',
'input' : '''
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
''',
'p1' : 11048,
'p2' : 64,
},
 
]
 
#################
wall = '#'
hall = '.'
d90 = {
    'E': ['S','N'],
    'S': ['W','E'],
    'W': ['N','S'],
    'N': ['E','W'],
}
 
mkey = lambda pos, dir : str(pos) + dir
large_cost = 999999
iterations = 0
 
def solve(aoc_input, part1=True, part2=True, attr=None) :
    maze = Grid.from_string(aoc_input)
    start_pos = (1, maze.dim_y-2)
    end_pos   = (maze.dim_x-2, 1)
    visited = {}
    assert maze.at_is(start_pos, 'S')
    assert maze.at_is(end_pos, 'E')
    maze.set(end_pos, hall)
    #print(maze, start_pos, end_pos)
    sys.setrecursionlimit(100000)
    p1_result, path = run_maze(maze, visited, start_pos, 'E', end_pos, 0)
    #print (path)
    p2_result = len(set(path))
 
    for p in set(path) :
        maze.set(p, 'O')
    print(f"Solved: in {iterations} iterations")
    #print(maze)
    return p1_result, p2_result
 
def run_maze (maze, visited,  pos, dir, end, cost) :
    global iterations
    iterations += 1
    #print(pos, dir, cost)
    #m = maze.copy()
    #m.set(pos,dir)
    #print (m)
    #c = sys.stdin.read(1)
    path = [pos]
 
    if cost > 200000 : return 0, []
 
    if pos == end :
        #print (f'Found END at {pos} with {cost}')
        return cost, path
 
    dirs = dirs_possible(maze, pos, dir)
    while len(dirs) == 1 :
        # only one way to go - it's a corridor, walk to the next junction or dead end
        pos = step(pos, dirs[0])
        path.append(pos)
        cost += (1 if dirs[0] == dir else 1001)
        dir = dirs[0]
        #print (f'stepped {dirs[0]} to {pos} cost {cost}')
        if pos == end :
            #print (f'Found END at {pos} with {cost}')
            return cost, path
        dirs = dirs_possible(maze, pos, dirs[0])
 
    if len(dirs) == 0 :
        #print (f'dead end at {pos}')
        return 0, [] # dead end
 
    # More  than one direction: a junction
 
    if mkey(pos,dir) in visited :
        if cost > visited[mkey(pos,dir)] :
            # Been here cheaper already
            #print (f'too expensive at {pos}  cost {cost}')
            return 0 , []
    else :
        # Check if we've seen this from another side -> then it can be a bit more expensive, but not massively so (?)
        for d in dirs :
            if mkey(pos,d) in visited :
                if cost > visited[mkey(pos,d)] + 1000:
                    #print (f'too expensive at {pos}  cost {cost}')
                    return 0 , []
 
    visited[mkey(pos,dir)] = cost
    #print (visited)
 
    # Go down all junctions
    least_cost = large_cost
    path_tmp = []
    for d in dirs :
        c, p = run_maze(maze, visited, step(pos, d), d, end, cost + (1 if d == dir else 1001))
        #print(f'CAME BACK with {c}')
        if c == 0 or c > least_cost : continue
       
        if c < least_cost :
            path_tmp = p
        else :
            #print (f"Found two equal ways at {pos}")
            path_tmp += p
        least_cost = c
 
    path += path_tmp
   
    if least_cost != large_cost :
        return least_cost, path
    else :
        return 0, []


def dirs_possible(maze, pos, dir) :
    possible = []
    for d in [ dir, d90[dir][0], d90[dir][1]] :
        if maze.at_is(step(pos, d), '.') : possible.append(d)
    return possible
 
#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]
 
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
