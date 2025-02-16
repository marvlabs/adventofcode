#!python3
'''Maze solver functions
Test different path finders  
'''
import heapq
from grid import Grid, step

#################################
# BFS : Flood fill maze walk: 
# Fill the maze step by step from start, return the nr of steps to find the pos
def flood_it(maze, start, end, wall='#') :
    nr_of_steps = -1 # because we also do a step to reach the start
    to_visit = [start]
    seen = set()

    while len(to_visit) :
        nr_of_steps += 1
        next_positions = set()

        for pos in to_visit :
            if pos == end : return nr_of_steps
            seen.add(pos)
            next_positions.update( neighbour_pos for _, neighbour_pos, tile in maze.valid_neighbours90(pos) if neighbour_pos not in seen and tile != wall )

        to_visit = next_positions

    return None
#################################

##########################
mc_distance = lambda p1, p2: abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

# A-star to search one end position - check every position:
def a_star_all(maze, start_pos, end_pos, wall='#') :
    counter = 0
    visited = set()
    unvisited = { start_pos : (0, mc_distance(start_pos, end_pos)) }

    while len(unvisited) :
        # Find the node with the lowest cost: An updatable priority queue would be nice here
        # Like Dijkstra, but we take the lowest cost so far and add the heuristic cost to the target (Monte Carlo Distance)
        pos = None; cost = 1E6; ch = None
        for p, ceha in unvisited.items() :
            pos, cost, ch = (p, ceha[0], ceha[1]) if not pos or ceha[1] < ch else (pos, cost, ch)

        counter += 1

        del unvisited[pos]
        visited.add(pos)

        for _, neighbour_pos, tile in maze.valid_neighbours90(pos) :
            if tile == wall : continue
            if neighbour_pos in visited : continue
            if neighbour_pos in unvisited and cost >= unvisited[neighbour_pos][0] : continue
            if neighbour_pos == end_pos : return cost+1 #print("d_r checked", counter) ; 
            unvisited[neighbour_pos] = (cost+1 , cost+1+mc_distance(neighbour_pos, end_pos))

    return None

def a_star_edge(maze, start_pos, end_pos, wall='#') :
    counter = 0
    visited = set()
    unvisited = { start_pos : (0, mc_distance(start_pos, end_pos)) }

    while len(unvisited) :
        # Find the node with the lowest cost: An updatable priority queue would be nice here
        pos = None; cost = 1E6; ch = None
        for p, ceha in unvisited.items() :
            pos, cost, ch = (p, ceha[0], ceha[1]) if not pos or ceha[1] < ch else (pos, cost, ch)

        counter += 1

        del unvisited[pos]
        visited.add(pos)

        for dir, neighbour_pos, tile in maze.valid_neighbours90(pos) :
            if tile == wall : continue
            # We try to walk this corridor from this next position, until either dead-end or next junction or end
            # This optimizes a lot of corridor tiles if there are long corridors. Only worth it if corridors longer 10 or so?
            neighbour_pos, next_cost = walk_edge(maze, neighbour_pos, dir, cost+1, end_pos, wall)
            if not neighbour_pos : continue
            if neighbour_pos == end_pos : return next_cost #print("d_r_e checked", counter) ;
            if neighbour_pos in visited : continue
            if neighbour_pos in unvisited and next_cost >= unvisited[neighbour_pos][0] : continue

            unvisited[neighbour_pos] = (next_cost , next_cost+mc_distance(neighbour_pos, end_pos))
    return None
##########################
# Djikstra to search for one end position - check every position:
def djikstra_real_all(maze, start_pos, end_pos, wall='#') :
    counter = 0
    visited = set()
    unvisited = { start_pos : 0 }

    while len(unvisited) :
        # Find the node with the lowest cost: An updatable priority queue would be nice here
        pos = None; cost = 1E6
        for p, c in unvisited.items() :
            pos, cost = (p, c) if not pos or c < cost else (pos, cost)

        counter += 1

        del unvisited[pos]
        visited.add(pos)

        for _, neighbour_pos, tile in maze.valid_neighbours90(pos) :
            if tile == wall : continue
            if neighbour_pos in visited : continue
            if neighbour_pos in unvisited and cost >= unvisited[neighbour_pos] : continue
            if neighbour_pos == end_pos : return cost+1 #print("d_r checked", counter) ; ; 
            unvisited[neighbour_pos] = cost+1

    return None


def djikstra_real_edge(maze, start_pos, end_pos, wall='#') :
    counter = 0
    visited = set()
    unvisited = { start_pos : 0 }

    while len(unvisited) :
        # Find the node with the lowest cost: An updatable priority queue would be nice here
        pos = None; cost = 1E6
        for p, c in unvisited.items() :
            pos, cost = (p, c) if not pos or c < cost else (pos, cost)

        counter += 1

        del unvisited[pos]
        visited.add(pos)

        for dir, neighbour_pos, tile in maze.valid_neighbours90(pos) :
            if tile == wall : continue
            # We try to walk this corridor from this next position, until either dead-end or next junction or end
            # This optimizes a lot of corridor tiles if there are long corridors. Only worth it if corridors longer 10 or so?
            neighbour_pos, next_cost = walk_edge(maze, neighbour_pos, dir, cost+1, end_pos, wall)
            if not neighbour_pos : continue
            if neighbour_pos == end_pos : return next_cost #print("d_r_e checked", counter) ;
            if neighbour_pos in visited : continue
            if neighbour_pos in unvisited and next_cost >= unvisited[neighbour_pos] : continue

            unvisited[neighbour_pos] = next_cost
    return None

def walk_edge(maze, pos, dir, cost, end_pos, wall) :
    while True :
        if pos == end_pos : return pos, cost # Found the target
        
        next_steps = [ fn for fn in maze.valid_neighbours90(pos) if fn[2] != wall ]
        if len(next_steps) == 1 : return None, None # dead end only back possible
        if len(next_steps)  > 2 : return pos, cost  # junction

        # We can step on. Make sure we don't step backwards
        next_step = next_steps[0] if next_steps[0][0] != d180[dir] else next_steps[1]
        dir = next_step[0]
        pos = next_step[1]
        cost += 1



def djikstra_edge_o(maze, start_pos, end_pos, wall='#') :
    start_node = { 'pos' : start_pos, 'cost' : 0 , 'edge': [start_pos]}
    visited = {}
    unvisited = []
    counter = 0
    heapq.heappush(unvisited, ( start_node['cost'], 0, start_node ) )
   
    while len(unvisited) :
        _, _, node = heapq.heappop(unvisited) # uses the cost as min and a dummy tie breaker
        if nkey(node) in visited : continue
        if node['pos'] == end_pos :
            #print ("deo", counter)
            return node['cost']#, path_from_node(node)

        visited[nkey(node)] = node

        dirs = dirs_possible(maze, node['pos'], None)
        for d in dirs :
            next_node = next_junction_ep(maze, node, d, end_pos, edge_cost = 1)
            if next_node is None : continue
            if nkey(next_node) in visited : continue

            if next_node['pos'] == end_pos :
                #print ("deo", counter)
                return next_node['cost']#, path_from_node(node)
            
            counter += 1 # as tie-breaker in the heapq
            heapq.heappush(unvisited, ( next_node['cost'], counter, next_node ) )

    return None


def djikstra_edge(maze, start_pos, end_pos, wall='#') :
    start_node = { 'pos' : start_pos, 'dir' : None , 'cost' : 0 , 'come_from' : [] , 'edge': [start_pos]}
    visited = {}
    unvisited = []
    counter = 0
    heapq.heappush(unvisited, ( start_node['cost'], 0, start_node ) )
   
    while len(unvisited) :
        _, _, node = heapq.heappop(unvisited) # uses the cost as min and a dummy tie breaker
        if nkey(node) in visited : continue
        if node['pos'] == end_pos :
            #print ("de ", counter)
            return node['cost']#, path_from_node(node)

        visited[nkey(node)] = node

        dirs = dirs_possible(maze, node['pos'], node['dir'])
        for d in dirs :
            next_node = next_junction_ep(maze, node, d, end_pos, edge_cost = 1)
            if next_node is None : continue
            if nkey(next_node) in visited : continue
            counter += 1 # as tie-breaker in the heapq
            heapq.heappush(unvisited, ( next_node['cost'], counter, next_node ) )

    return None

nkey = lambda node : str(node['pos'])

# Instead of Dijkstraing every field in the maze, we compress it to edges and junctions
# This delivers a junction node, stepping from pos in dir, and sets the cost, path taken and where it came from
def next_junction_ep(maze, node, dir, end_pos, edge_cost, wall='#') :
    next_pos = step(node['pos'], dir)
    edge_path = [next_pos]
    dirs = dirs_possible(maze, next_pos, dir)
    while len(dirs) == 1 :
        # only one way to go - it's a corridor, walk to the next junction or dead end
        next_pos = step(next_pos, dirs[0])
        edge_path.append(next_pos)
        edge_cost += 1
        dir = dirs[0]
        if next_pos == end_pos :
            # End Pos is also a node, even if it doesn't have a junction
            #print (f'Found END node at {next_pos} with {node['cost'] + edge_cost}')
            break
        dirs = dirs_possible(maze, next_pos, dirs[0])

    if len(dirs) == 0 and next_pos != end_pos: # dead end
        return None
    
    return { 'pos' : next_pos, 'dir' : dir , 'cost' : node['cost'] + edge_cost , 'come_from' : [node] , 'edge': edge_path }

d90 = {
    'E': ['S','N'],
    'S': ['W','E'],
    'W': ['N','S'],
    'N': ['E','W'],
}
d180 = { 'E': 'W', 'S': 'N', 'W': 'E', 'N': 'S' }

def dirs_possible(maze, pos, dir, wall='#') :
    possible = []
    for d in [ dir, d90[dir][0], d90[dir][1]] if dir else [ 'E', 'S', 'W', 'N']:
        if not maze.valid(step(pos, d)): continue
        if not maze.at_is(step(pos, d), wall) : possible.append(d)
    return possible

#################################
if __name__ == '__main__' :
    import timeit
    from grid import Grid

    all_algs = ['a_star_edge', 'a_star_all', 'djikstra_edge', 'flood_it', 'djikstra_real_edge', 'djikstra_real_all']
    n_runs = 50
    #########
    print("----")
    print('2016 day 24')

    with open('input/24.txt') as f: s = f.read()
    maze = Grid.from_string(s)
    locations = { int(maze.get(pos)) : pos for pos in maze.all_pos() if maze.get(pos).isdigit() }

    #for finder in ('djikstra_edge_o','flood_it', 'djikstra_edge', ) :
    for finder in (all_algs) :
        assert globals()[finder](maze, locations[0], locations[1]) == 198
        print(f'{finder:20s}', timeit.timeit(finder + "(maze, locations[0], locations[1])", setup="from __main__ import maze, locations,"+finder, number=n_runs))

    #########
    print("----")
    print('2024 day 16')
    with open('../2024/input/16.txt') as f: s = f.read()
    maze = Grid.from_string(s)
    start_pos = (1, maze.dim_y-2)
    end_pos   = (maze.dim_x-2, 1)
    for finder in (all_algs) :
        assert globals()[finder](maze, start_pos, end_pos) == 428
        print(f'{finder:20s}', timeit.timeit(finder + "(maze, start_pos, end_pos)", setup="from __main__ import maze, start_pos, end_pos,"+finder, number=n_runs))


    #########
    print("----")
    print('2024 day 20')
    with open('../2024/input/20.txt') as f: s = f.read()
    maze = Grid.from_string(s)
    for p in maze.all_pos() :
        if maze.at_is(p, 'S') : 
            #maze.set(p, hall)
            start_pos = p
        if maze.at_is(p, 'E') :
            #maze.set(p, hall)
            end_pos = p    
    for finder in (all_algs) :
        assert globals()[finder](maze, start_pos, end_pos) == 9352
        print(f'{finder:20s}', timeit.timeit(finder + "(maze, start_pos, end_pos)", setup="from __main__ import maze, start_pos, end_pos,"+finder, number=n_runs))
