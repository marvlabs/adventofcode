#!python3
'''AoC 2024 Day 16'''
from grid import Grid, step
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '16',
    'url'           :   'https://adventofcode.com/2024/day/16',
    'name'          :   "Reindeer Maze: lots of ways",
    'difficulty'    :   'D3',
    'learned'       :   'Patience in recursion? Nope. Dijkstra.',
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
'p2' : None#64,
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
 
def solve(aoc_input, part1=True, part2=True, attr=None) :
    maze = Grid.from_string(aoc_input)
    start_pos = (1, maze.dim_y-2)
    end_pos   = (maze.dim_x-2, 1)
    assert maze.at_is(start_pos, 'S')
    assert maze.at_is(end_pos, 'E')
    maze.set(end_pos, hall)

    p1_result, path = dijkstra_maze(maze, start_pos, 'E', end_pos)
    p2_result = len(path)
 
    return p1_result, p2_result


nkey = lambda node : str(node['pos']) + node['dir']
nstr = lambda node : f'{node["pos"]} {node["dir"]} {node["cost"]}'

def dijkstra_maze(maze, start_pos, start_dir, end_pos) :
    start_node = { 'pos' : start_pos, 'dir' : start_dir , 'cost' : 0 , 'come_from' : [] , 'edge': [start_pos]}
    visited = {}
    unvisited = [start_node]
    end_node = None
   
    while len(unvisited) :
        # Find the node with the lowest cost: An updatable priority queue would be nice here
        node = None
        for n in unvisited : 
            node = n if not node or n['cost'] < node['cost'] else node
        unvisited.remove(node)

        if nkey(node) in visited : 
            # We've already visited this node. This path cannot be cheaper. 
            # But it can be the same cost -> then add its heritage to the come_from list of the already found one as additional possible path
            if node['cost'] == visited[nkey(node)]['cost'] :
                visited[nkey(node)]['come_from'].extend(node['come_from'])
                visited[nkey(node)]['edge'].extend(node['edge'])
            continue

        visited[nkey(node)] = node

        dirs = dirs_possible(maze, node['pos'], node['dir'])
        for d in dirs :
            next_node = next_junction(maze, node, d, end_pos, edge_cost = (1 if node['dir'] == d else 1001))
            if next_node is None : continue
            unvisited.append(next_node)

        if node['pos'] == end_pos and not end_node:
            # Found the cheapest route. We could return. BUT:
            # Then there would be an uncovered edge case: 
            #   if this very end_pos could be reached with equal cost from one of the next nodes, we would miss it
            # Therefore, continue and find all other nodes, but store this one as the solution.
            end_node = node
            
    return end_node['cost'], path_from_node(end_node)


def path_from_node(node) :
    # Go back through the came_from list to gobble up the path back to the start for p2
    path = node['edge']
    node_paths = node['come_from']
    while len(node_paths) :
        n = node_paths.pop()
        path.extend(n['edge'])
        node_paths.extend(n['come_from'])
    return set(path)


# Instead of Dijkstraing every field in the maze, we compress it to edges and junctions
# This delivers a junction node, stepping from pos in dir, and sets the cost, path taken and where it came from
def next_junction(maze, node, dir, end_pos, edge_cost) :
    next_pos = step(node['pos'], dir)
    edge_path = [next_pos]
    dirs = dirs_possible(maze, next_pos, dir)
    while len(dirs) == 1 :
        # only one way to go - it's a corridor, walk to the next junction or dead end
        next_pos = step(next_pos, dirs[0])
        edge_path.append(next_pos)
        edge_cost += (1 if dirs[0] == dir else 1001)
        dir = dirs[0]
        if next_pos == end_pos :
            # End Pos is also a node, even if it doesn't have a junction
            #print (f'Found END node at {next_pos} with {node['cost'] + edge_cost}')
            break
        dirs = dirs_possible(maze, next_pos, dirs[0])

    if len(dirs) == 0 and next_pos != end_pos: # dead end
        return None
    
    return { 'pos' : next_pos, 'dir' : dir , 'cost' : node['cost'] + edge_cost , 'come_from' : [node] , 'edge': edge_path }


def dirs_possible(maze, pos, dir) :
    possible = []
    for d in [ dir, d90[dir][0], d90[dir][1]] :
        if maze.at_is(step(pos, d), hall) : possible.append(d)
    return possible
 
#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]
 
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
