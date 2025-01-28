#!python3
'''AoC 2024 Day 20'''
from grid import Grid, step
import anim
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '20',
    'url'           :   'https://adventofcode.com/2024/day/20',
    'name'          :   "Race Condition: Path this Maze",
    'difficulty'    :   'D2',
    'learned'       :   'Not much to optimize here, methinks',
    't_used'        :   '40',
    'result_p1'     :   1289,
    'result_p2'     :   982425,
}
#############
TESTS = [
{
'name'  : 'Maze1',
'input' : '''
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
''',
'testattr' : (9,71), # 8 cheats save more than 9ps for p1, 29 save more than 71 for p2
'p1' : 10,
'p2' : 29,
},
]
 
#################
wall = '#'
hall = '.'
d_cheat = {
    'E': (2,0),
    'S': (0,2),
    'W': (-2,0),
    'N': (0,-2),
}

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result= p2_result = 0
    maze = Grid.from_string(aoc_input)
    for p in maze.all_pos() :
        if maze.at_is(p, 'S') : 
            maze.set(p, hall)
            start_pos = p
        if maze.at_is(p, 'E') :
            maze.set(p, hall)
            end_pos = p

    path = run_maze(maze, start_pos, end_pos)

    anim_race(maze, path, 20, 100)
    p1_result = find_from_maze_p1(maze, path, at_least=(100 if not attr else attr[0]))
    p2_result = find_from_path_with_skip_ahead(path, 20, at_least=(100 if not attr else attr[1]))
    #p1_result = find_from_maze_generalized(maze, path, 2, at_least=(100 if not attr else attr[0]))
    #p2_result = find_from_maze_generalized(maze, path, 20, at_least=(100 if not attr else attr[1]))

    return p1_result, p2_result

#### Animation
dim = 141
a = anim.AnimGrid(anim.Screen(dim*8, dim*8+50, 'Race Condition'), dim, dim,
    use_chars=False, status_area=50, 
    title='AOC 2024-20 Race Condition', movie = "AOC_2024-20_Race_Condition")
a.color_map = { '.': 'BLACK', '#': 'DARK_BLUE', 'O': 'ORANGE', ' ': 'DARK_GRAY', '-': 'GREEN', 'x': 'RED', 'default': 'PINK' }

def anim_race(maze, path, max_dist, at_least=100) :
    nr = winner = in_goal = race_won = 0
    racers = []
    for src_idx in range(len(path)) :
        pos = path[src_idx]

        maze.set(pos, 'O')
        for idx in racers :
            maze.set(path[idx], 'x')
        if race_won : maze.set(path[-1], '-')
        if src_idx % 2 == 0 or src_idx == len(path)-1: 
            a.draw(maze, 1, f'Peloton at: {src_idx:5d}   Cheaters: {len(racers):4d}   Winner Time: {winner:4d}   In Goal: {in_goal:4d}')   
        racers_next = []
        for idx in racers :
            maze.set(path[idx], '.')
            if idx < len(path)-1 :
                racers_next.append(idx+1)
            if idx == len(path)-1 :
                in_goal += 1
                if not race_won  :
                    race_won = len(path)-1
                    winner = src_idx
        racers = []
        racers.extend(racers_next)

        if src_idx % 50 == 0 :
            dst_idx = src_idx + at_least
            best_cheat = 0
            best_cheat_idx = 0
            while dst_idx < len(path) :
                dist = distance(pos, path[dst_idx])
                cheat = dst_idx - src_idx - dist
                if dist <= max_dist and  cheat >= at_least :
                    nr += 1
                    if cheat > best_cheat :
                        best_cheat = cheat
                        best_cheat_idx = dst_idx
                # Skip ahead if possible. Only start checking again when it's possible that we came close enough
                dst_idx += dist-max_dist if dist > max_dist else 1

            if best_cheat : 
                #print(f'{src_idx} {best_cheat_idx} {best_cheat} nr of racers {len(racers)}')
                racers.append(best_cheat_idx)

    a.draw(maze, 3000, f'Peloton at: {src_idx:5d}   Cheaters: {len(racers):4d}   Winner Time: {winner:4d}   In Goal: {in_goal:4d}')   
    a.save_movie(fps=120)

    return nr

####


distance = lambda p1, p2 : abs(p2[0]-p1[0]) + abs(p2[1]-p1[1])

# From each position in the path: Check positions sufficiently further along: are they reachable by a cheat and worth it?
# Skip-Ahead optimized! 
#   If a position it too far ahead, skip n positions in the list to close the distance.
#   (Any next position in the list can come closer max 1 step per position.)
# This uses only the path,
# (Also works for part 1, but slightly slower than the dedicated function)
def find_from_path_with_skip_ahead(path, max_dist, at_least=100) :
    nr = 0
    for src_idx in range(0, len(path)-at_least) :
        pos = path[src_idx]
        dst_idx = src_idx + at_least
        while dst_idx < len(path) :
            dist = distance(pos, path[dst_idx])
            if dist <= max_dist and  dst_idx - src_idx - dist >= at_least :
                nr += 1

            # Skip ahead if possible. Only start checking again when it's possible that we came close enough
            dst_idx += dist-max_dist if dist > max_dist else 1
    return nr

# From each position in the path: Check the fields reachable by a two-step straight cheat and count if worth it
# This uses the marked fields in the maze
def find_from_maze_p1(maze, path, at_least=100) :
    nr = 0
    for p in path :
        for cheat_dir in d_cheat.values() :
            cheat_pos = (p[0]+cheat_dir[0], p[1]+cheat_dir[1])
            cost = maze.get(cheat_pos)
            if not cost or isinstance(cost,str) : continue
            cost_field = maze.get(p)
            if cost - cost_field - 2 >= at_least:
                nr += 1
    return nr


# Record the path, mark the visited fields with the cost
def run_maze(maze, start_pos, end_pos) :
    cost = 0
    pos = start_pos
    maze.set(pos, cost)

    path = [pos]
    while pos != end_pos :
        for dir, tile in maze.neighbours90(pos).items() :
            if tile != hall : continue
            pos = step(pos, dir)
            cost += 1
            maze.set(pos, cost)
            path.append(pos)

    return path


# # Alternate p2: like p1, but iterate over all fields in range of max_dist steps
# # Also works for p2
# def find_from_maze_generalized(maze, path, max_dist,at_least=100) :
#     nr = 0
#     for p in path :
#         cost = maze.get(p)
#         for x in range(-max_dist, max_dist+1) :
#             for y in range(-max_dist, max_dist+1) :
#                 way = abs(x) +abs(y)
#                 if way < 2 or way > max_dist : continue
#                 cost_field = maze.get((p[0]+x, p[1]+y))
#                 if not cost_field or isinstance(cost_field, str) : continue
#                 if cost_field - cost - way >= at_least:
#                     nr += 1
#     return nr


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]
 
    aoc.init(puzzle)
    #aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)

