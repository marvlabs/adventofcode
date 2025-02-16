#!python3
'''AoC 2016 Day 24'''
from grid import Grid, step
#import heapq
from itertools import permutations
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '24',
    'url'           :   'https://adventofcode.com/2016/day/24',
    'name'          :   "Air Duct Spelunking - Crawl those ducts",
    'difficulty'    :   'D2',
    'learned'       :   'Again, why Dijkstra when flooding is faster...',
    't_used'        :   '90',
    'result_p1'     :   462, 
    'result_p2'     :   676,
}
#############
TESTS = [
{
    'name'  : '4-locations',
    'input' : 
    '''
###########
#0.1.....2#
#.#######.#
#4.......3#
###########''',
    'p1' : 14,
    'p2' : None,
},
]
#################
wall = '#'
hall = '.'

def solve(aoc_input, part1=True, part2=True, attr=None) :
    maze = Grid.from_string(aoc_input)

    # Find all locations in maze: single digits, not hall nor wall
    locations = { int(maze.get(pos)) : pos for pos in maze.all_pos() if maze.get(pos).isdigit() }

    # Find the cost of reaching every other digit (location) from each digit:
    # One search returns a cost-list (digit-indexed) when it found all n locations from a given start location 
    # (i.e. for 0 : [0, 2, 8, 10, 2] - it costs 2 to reach '1' and 8 to reach '2' in the example)
    all_cost = [ flood_it(maze, locations[i], len(locations)) for i in range(0, len(locations))]
    #print (all_cost)
    # Compute the min of the cost of all possible paths from location 0 to all others (and back to 0 for p2)
    # (i.e. paths 0-1-2-3-4 / 0-2-1-3-4 / 0-3-1-2-4 ...)
    p1_result = min(sum(all_cost[path[i]][path[i+1]] for i in range(len(path)-1)) for path in ( [0, *p]    for p in permutations(range(1,len(locations))) ) )
    p2_result = min(sum(all_cost[path[i]][path[i+1]] for i in range(len(path)-1)) for path in ( [0, *p, 0] for p in permutations(range(1,len(locations))) ) )

    return p1_result, p2_result


# Flood fill maze walk: fill the maze step by step from start, return the nr of steps to find the 'digit' locations
def flood_it(maze, start, nr_of_locations) :
    locations = [None]*nr_of_locations
    nr_of_steps = -1 # because we also do a step to reach the start
    to_visit = [start]
    seen = set()

    while len(to_visit) :
        nr_of_steps += 1
        next_positions = set()

        for pos in to_visit :
            seen.add(pos)
            next_positions.update( neighbour_pos for _, neighbour_pos, tile in maze.valid_neighbours90(pos) if neighbour_pos not in seen and tile != wall )

            tile = maze.get(pos)
            if tile != hall and tile != wall :
                locations[int(tile)] = nr_of_steps
                if not None in locations: return locations # no need to fill any more when all locations have been found

        to_visit = next_positions

    return locations


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)


##########################
# Djikstra which returns a list of found positions: does only stop if n found

# # This Djikstra only returns when it finds the way to n (nr_of_location) targets (all denoted by a digit in the maze)
# nkey = lambda node : str(node['pos'])
# def dijkstra_maze(maze, start_pos, nr_of_locations) :
#     start_node = { 'pos' : start_pos, 'dir' : None , 'cost' : 0 , 'come_from' : [] , 'edge': [start_pos]}
#     visited = {}
#     unvisited = []
#     locations = [None]*nr_of_locations
#     counter = 0
#     heapq.heappush(unvisited, ( start_node['cost'], 0, start_node ) )
   
#     while len(unvisited) :
#         _, _, node = heapq.heappop(unvisited) # uses the cost as min and a dummy tie breaker
#         if nkey(node) in visited : continue
#         tile = maze.get(node['pos'])
#         if tile != hall and tile != wall :
#             if locations[int(tile)] == None :
#                 locations[int(tile)] = node['cost']
#                 if not None in locations:
#                     return locations

#         visited[nkey(node)] = node

#         dirs = dirs_possible(maze, node['pos'], node['dir'])
#         for d in dirs :
#             next_node = next_junction(maze, node, d, edge_cost = 1)
#             if next_node is None : continue
#             if nkey(next_node) in visited : continue
#             counter += 1 # as tie-breaker in the heapq
#             heapq.heappush(unvisited, ( next_node['cost'], counter, next_node ) )

#     return locations


# # Instead of Dijkstraing every field in the maze, we compress it to edges and junctions
# # This delivers a junction node, stepping from pos in dir, and sets the cost, path taken and where it came from
# def next_junction(maze, node, dir, edge_cost) :
#     next_pos = step(node['pos'], dir)
#     edge_path = [next_pos]
#     dirs = dirs_possible(maze, next_pos, dir)
#     found_location = False
#     while len(dirs) == 1 :
#         # only one way to go - it's a corridor, walk to the next junction or dead end
#         next_pos = step(next_pos, dirs[0])
#         edge_path.append(next_pos)
#         edge_cost += 1
#         dir = dirs[0]
        
#         tile = maze.get(next_pos)
#         if tile != hall and tile != wall :
#             # A location is also a node, even if it doesn't have a junction
#             #print (f'Found LOCATION node {tile} at {next_pos} with {node['cost'] + edge_cost}')
#             found_location = True
#             break        
        
#         dirs = dirs_possible(maze, next_pos, dirs[0])

#     if len(dirs) == 0 and not found_location: # dead end
#         return None

#     return { 'pos' : next_pos, 'dir' : dir , 'cost' : node['cost'] + edge_cost , 'come_from' : [node] , 'edge': edge_path }

# d90 = {
#     'E': ['S','N'],
#     'S': ['W','E'],
#     'W': ['N','S'],
#     'N': ['E','W'],
# }

# def dirs_possible(maze, pos, dir) :
#     possible = []
#     for d in [ dir, d90[dir][0], d90[dir][1]] if dir else [ 'E', 'S', 'W', 'N']:
#         if not maze.valid(step(pos, d)): continue
#         if not maze.at_is(step(pos, d), wall) : possible.append(d)
#     return possible


##########################
# Djikstra to search for one end position:

# def dijkstra_maze_ep(maze, start_pos, end_pos) :
#     start_node = { 'pos' : start_pos, 'dir' : None , 'cost' : 0 , 'come_from' : [] , 'edge': [start_pos]}
#     visited = {}
#     unvisited = []
#     counter = 0
#     heapq.heappush(unvisited, ( start_node['cost'], 0, start_node ) )
   
#     while len(unvisited) :
#         _, _, node = heapq.heappop(unvisited) # uses the cost as min and a dummy tie breaker
#         if nkey(node) in visited : continue
#         if node['pos'] == end_pos :
#             return node['cost'], path_from_node(node)

#         visited[nkey(node)] = node

#         dirs = dirs_possible(maze, node['pos'], node['dir'])
#         for d in dirs :
#             next_node = next_junction_ep(maze, node, d, end_pos, edge_cost = 1)
#             if next_node is None : continue
#             if nkey(next_node) in visited : continue
#             counter += 1 # as tie-breaker in the heapq
#             heapq.heappush(unvisited, ( next_node['cost'], counter, next_node ) )

#     return None

# # Instead of Dijkstraing every field in the maze, we compress it to edges and junctions
# # This delivers a junction node, stepping from pos in dir, and sets the cost, path taken and where it came from
# def next_junction_ep(maze, node, dir, end_pos, edge_cost) :
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

# def path_from_node(node) :
#     # Go back through the came_from list to gobble up the path back to the start for p2
#     path = node['edge']
#     node_paths = node['come_from']
#     while len(node_paths) :
#         n = node_paths.pop()
#         path.extend(n['edge'])
#         node_paths.extend(n['come_from'])
#     return set(path)
##########################
