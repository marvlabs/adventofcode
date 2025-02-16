#!python3
'''AoC 2016 Day 13'''
from grid import Grid, step
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '13',
    'url'           :   'https://adventofcode.com/2016/day/13',
    'name'          :   "A Maze of Twisty Little Cubicles - generated Maze",
    'difficulty'    :   'D2',
    'learned'       :   'Why Dijkstra when Flood-fill...',
    't_used'        :   '40',
    'result_p1'     :   90, 
    'result_p2'     :   135,
}
#############
TESTS = [
{
        'name'  : 'maze-10',
        'input' : '''10''',
        'p1' : 11,
        'p2' : None,
        'testattr' : (7,4)
},
]

#################
wall = '#'
hall = '.'

def create_maze(dim, seed) :
    maze = Grid(dim, dim, hall)
    for pos in maze.all_pos() :
        x, y = pos
        val = x*x + 3*x + 2*x*y + y + y*y + seed
        nr_of_bits = sum( [ b=='1' for b in f'{val:b}' ] )
        if nr_of_bits % 2 == 1 :
            maze.set(pos, wall)
    return maze

# Flood fill search: fill the maze step by step
# Returns how many filled after n steps and how may steps needed until target reached
def flood_it(maze, start, end, n_steps) :
    end_found = n_steps_found = None
    nr_of_steps = -1 # because we also do a step to reach the start
    to_visit = [start]
    seen = set()

    while True :
        nr_of_steps += 1
        next_positions = set()

        while len(to_visit) :
            pos = to_visit.pop()
            seen.add(pos)
            if pos == end : 
                end_found = nr_of_steps

            for _, neighbour_pos, tile in maze.valid_neighbours90(pos) :
                if neighbour_pos not in seen and tile == hall :
                    next_positions.add(neighbour_pos)

        if nr_of_steps == n_steps : n_steps_found = len(seen)
        if n_steps_found and end_found : return end_found, n_steps_found
        
        to_visit = next_positions


def solve(aoc_input, part1=True, part2=True, attr=None) :
    target = attr if attr else (31,39) # for test input
    maze = create_maze(50, int(aoc_input))
    p1_result, p2_result = flood_it(maze, (1,1), target, 50)

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



# I first re-used a Dijkstra solution. REALLY not necessary for this...
# But hey, maybe we're going to need it later...

# import heapq
# nkey = lambda node : str(node['pos'])
# def dijkstra_maze(maze, start_pos, start_dir, end_pos) :
#     start_node = { 'pos' : start_pos, 'dir' : start_dir , 'cost' : 0 , 'come_from' : [] , 'edge': [start_pos]}
#     visited = {}
#     unvisited = []
#     counter = 0
#     heapq.heappush(unvisited, ( start_node['cost'], 0, start_node ) )
   
#     while len(unvisited) :
#         _, _, node = heapq.heappop(unvisited) # uses the cost as min and a dummy tie breaker

#         if node['pos'] == end_pos :
#             return node['cost'], path_from_node(node)

#         visited[nkey(node)] = node

#         dirs = dirs_possible(maze, node['pos'], node['dir'])
#         for d in dirs :
#             next_node = next_junction(maze, node, d, end_pos, edge_cost = 1)
#             if next_node is None : continue
#             if nkey(next_node) in visited or nkey(next_node) in unvisited : continue
#             counter += 1 # as tie-breaker in the heapq
#             heapq.heappush(unvisited, ( next_node['cost'], counter, next_node ) )

#     return None


# def path_from_node(node) :
#     # Go back through the came_from list to gobble up the path back to the start for p2
#     path = node['edge']
#     node_paths = node['come_from']
#     while len(node_paths) :
#         n = node_paths.pop()
#         path.extend(n['edge'])
#         node_paths.extend(n['come_from'])
#     return set(path)


# # Instead of Dijkstraing every field in the maze, we compress it to edges and junctions
# # This delivers a junction node, stepping from pos in dir, and sets the cost, path taken and where it came from
# def next_junction(maze, node, dir, end_pos, edge_cost) :
#     next_pos = step(node['pos'], dir)
#     edge_path = [next_pos]
#     dirs = dirs_possible(maze, next_pos, dir)
#     while len(dirs) == 1 :
#         # only one way to go - it's a corridor, walk to the next junction or dead end
#         next_pos = step(next_pos, dirs[0])
#         edge_path.append(next_pos)
#         edge_cost += 1
#         dir = dirs[0]
#         if next_pos == end_pos :
#             # End Pos is also a node, even if it doesn't have a junction
#             #print (f'Found END node at {next_pos} with {node['cost'] + edge_cost}')
#             break
#         dirs = dirs_possible(maze, next_pos, dirs[0])

#     if len(dirs) == 0 and next_pos != end_pos: # dead end
#         return None
    
#     return { 'pos' : next_pos, 'dir' : dir , 'cost' : node['cost'] + edge_cost , 'come_from' : [node] , 'edge': edge_path }


# def dirs_possible(maze, pos, dir) :
#     possible = []
#     for d in [ dir, d90[dir][0], d90[dir][1]] :
#         if not maze.valid(step(pos, d)): continue
#         if maze.at_is(step(pos, d), hall) : possible.append(d)
#     return possible
 