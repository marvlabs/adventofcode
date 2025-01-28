#!python3
'''AoC 2024 Day 14'''
# from pprint import pprint as pp
import re
from grid import Grid
import anim
from os import system
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '14',
    'url'           :   'https://adventofcode.com/2024/day/14',
    'name'          :   "Restroom Redoubt: find the tree",
    'difficulty'    :   'D2',
    'learned'       :   'What\'s a tree?',
    't_used'        :   '30',
    'result_p1'     :   230686500,
    'result_p2'     :   7672,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3''',
        'testattr': (11,7),
        'p1' : 12,
        'p2' : None,
    },
]
#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    
    dim=attr if attr else (101,103)
    middle = (dim[0]//2, dim[1]//2)
    time = 100
    q1 = q2 = q3 = q4 = 0
    robots = []

    for string in aoc_input.splitlines()  :
        if string == '' : continue
        px, py, vx, vy = list(map(int, re.match(r'p=(.*),(.*) v=(.*),(.*)', string).groups()))
        pos_at_time = ((px + time*vx) % dim[0], (py + time*vy) % dim[1])
        
        if pos_at_time[0] < middle[0] and pos_at_time[1] < middle[1] : q1 += 1
        elif pos_at_time[0] > middle[0] and pos_at_time[1] < middle[1] : q2 += 1
        elif pos_at_time[0] < middle[0] and pos_at_time[1] > middle[1] : q3 += 1
        elif pos_at_time[0] > middle[0] and pos_at_time[1] > middle[1] : q4 += 1

        robots.append([px, py, vx, vy])
    
    p1_result = q1 * q2 * q3 * q4
    p2_result = animate_till(dim, robots, '#############')
    return p1_result, p2_result

a = anim.AnimGrid(anim.Screen(101*8, 103*8+50, 'Toilet Guards, slowed down'), 101, 103, use_chars=False, status_area=50,\
    title='Toilet Guards, slowed down',
)#movie = "AOC_2024-14_Toilet-Guards-XMAS-Tree")
a.color_map['#'] = 'GREEN'
def animate_till(dim, robots, pattern) :
    res = 0

    step = 150
    i=0
    for t in range(7671*step, 7672*step+75 ) :
        g = Grid(dim[0], dim[1], ' ')
        for px, py, vx, vy in robots :
            pos_at_time = (int((px + t/step*vx) % dim[0]), int((py + t/step*vy) % dim[1]))
            g.set(pos_at_time, '#')
        a.draw(g, 30)
        i+=1
        if str(g).find(pattern) >= 0: 
            res = t
            for dummy in range(10) :
                a.draw(g, 30)
                i+=1
    a.save_movie()
    return res
            



#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    #aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
