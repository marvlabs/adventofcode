#!python3
'''AoC 2015 Day 18'''
from grid import Grid
from queue import Queue, Empty
from threading import Thread
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '18',
    'url'           :   'https://adventofcode.com/2015/day/18',
    'name'          :   "Like a GIF For Your Yard - Game of Lights",
    'difficulty'    :   'D2',
    'learned'       :   'Python Class: made a Grid. Python threading is shite',
    't_used'        :   '30',
    'result_p1'     :   1061,
    'result_p2'     :   1006,
}
#############
TESTS = [
    {
        'name'  : '6x6 Grid',
        'input' : '''
.#.#.#
...##.
#....#
..#...
#.#..#
####..
''',
        'p1' : 4, # for 4 iterations
        'p2' : None,
        'testattr': 4
    },
    {
        'name'  : '6x6 Grid broken',
        'input' : '''
.#.#.#
...##.
#....#
..#...
#.#..#
####..
''',
        'p1' : None, 
        'p2' : 17, # for 5 iterations
        'testattr': 5
    },
]
#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    cycles = 100 if not attr else attr

    light_grid = Grid.from_string(aoc_input)
    for _ in range(cycles) :
        light_grid = animate_q(light_grid)
    p1_result = sum(light_grid.at_is(pos, '#') for pos in light_grid.all_pos())

    # Part 2: with stuck corners
    light_grid = Grid.from_string(aoc_input)
    set_corners(light_grid, '#')
    for _ in range(cycles) :
        light_grid = animate_q(light_grid)
        set_corners(light_grid, '#')
    p2_result = sum(light_grid.at_is(pos, '#') for pos in light_grid.all_pos())

    return p1_result, p2_result


def set_corners(g, val) :
    for pos in [(0,0), (0,g.dim_y-1), (g.dim_x-1,0), (g.dim_x-1,g.dim_y-1)] :
        g.set(pos, '#')


# def animate(g):
#     g_next = Grid(g.dim_x, g.dim_y)
#     for pos in (g_next.all_pos()) :
#         nr_of_n = sum([ 1 for light in g.neighbours(pos).values() if light == '#'])
#         g_next.set(pos,  '.' if (g.get(pos) == '#' and nr_of_n != 2 and nr_of_n !=3) or (g.get(pos) == '.' and nr_of_n != 3) else '#')
#     return g_next

def check_pos(i, g, g_next, q):
    while True :
        try :
            pos = q.get(block=False)
            nr_of_n = sum([ 1 for light in g.neighbours(pos).values() if light == '#'])
            g_next.set(pos,  '.' if (g.get(pos) == '#' and nr_of_n != 2 and nr_of_n !=3) or (g.get(pos) == '.' and nr_of_n != 3) else '#')
            #q.task_done()
            #print ('check_pos:', pos)
        except Empty:
            #print ('check_pos: done', i)
            return
        

def animate_q(g):
    '''Threaded version with a queue and workers is - shite.
    The Python Global Interpret Lock (GIL) blocks simultaneous access to the interpreter, thereby completely voiding threading benefits.
    (Unless you do stuff outside the interpreter, like network waits, numpy stuff etc.)'''
    g_next = Grid(g.dim_x, g.dim_y)
    q = Queue()
    for pos in (g_next.all_pos()) :
        q.put(pos)
    workers = [ Thread(target=check_pos, args=(i, g, g_next, q)) for i in range(5) ]
    for w in workers: w.start()
    for w in workers: w.join()
    #q.join()
    #print('animate_q: joined')
    return g_next

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)

