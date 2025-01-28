#!python3
import re
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '06',
    'url'           :   'https://adventofcode.com/2015/day/6',
    'name'          :   "Probably a Fire Hazard - Light array",
    'difficulty'    :   'D1',
    'learned'       :   'Python regex, slice, lambda functions, array <-> dict performance',
    't_used'        :   '45',
    'result_p1'     :   569999,
    'result_p2'     :   17836115,
}
#############
TESTS = [
 {
        'name'  : 'lights-1',
        'input' : '''
turn on 0,0 through 999,999
toggle 0,0 through 999,0
turn off 499,499 through 500,500
''',
        'p1' : 998996,
        'p2' : 1001996,
    },
    {
        'name'  : 'lights-2',
        'input' : '''
turn on 0,0 through 0,0
toggle 0,0 through 999,999
''',
        'p1' : 999999,
        'p2' : 2000001,
    },]

#############
DIM_X, DIM_Y = 1000, 1000

p1_func = {
    'turn on'   : lambda x : 1,
    'turn off'  : lambda x : 0,
    'toggle'    : lambda x : 0 if x else 1,
}
p2_func = {
    'turn on'   : lambda x : x+1,
    'turn off'  : lambda x : x-1 if x>0 else 0,
    'toggle'    : lambda x : x+2,
}

#################

def switch_lights(lights, x1, x2, y1, y2, mode_func) :
    '''Apply the mode-function to a rectangle (x / y ranges)
        param: ligths dict, x and y range, mode function
        changes: lights'''
    for y in range(y1, y2+1) :
        x_es = slice(y*DIM_X+x1, y*DIM_X+x2+1)
        lights[x_es] = map(mode_func, lights[x_es])


def solve(aoc_input, part1=True, part2=True, attr=None) :
    lights_p1 = [0]*DIM_X*DIM_Y
    lights_p2 = [0]*DIM_X*DIM_Y

    for string in aoc_input.splitlines() :
        if string == '' :
            continue
        instruction, x1, y1, x2, y2 = re.match(r'(.*) (\d+),(\d+) through (\d+),(\d+)', string).groups()
        switch_lights(lights_p1, int(x1), int(x2), int(y1), int(y2), p1_func[instruction])
        switch_lights(lights_p2, int(x1), int(x2), int(y1), int(y2), p2_func[instruction])

    return sum(lights_p1), sum(lights_p2)

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    assert p1_func['toggle'](1) == 0
    assert p1_func['toggle'](0) == 1
    assert p1_func['turn on'](0) == 1
    assert p1_func['turn on'](1) == 1
    assert p1_func['turn off'](1) == 0
    assert p1_func['turn off'](0) == 0
    assert p2_func['toggle'](1) == 3
    assert p2_func['toggle'](0) == 2
    assert p2_func['turn on'](0) == 1
    assert p2_func['turn on'](1) == 2
    assert p2_func['turn off'](2) == 1
    assert p2_func['turn off'](0) == 0

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)

# #####################
# # Version with dictionary. Index is a string-key from x/y
# # Works, but runs 19s , a bit slow.
# # Replaced by above flat array version with index x+y*1000 , sliced / mapped runs in 2s
# def key(pos) :
#     return str(pos[0]) + '/' + str(pos[1])

# def switch_lights_dict(lights, range_x, range_y, mode_func) :
#     '''Apply the mode-function to a rectangle (x / y ranges)
#         param: ligths dict, x and y range, mode function
#         changes: lights'''
#     for x in range_x :
#         for y in range_y :
#             k = key((x, y))
#             lights[k] = mode_func(lights.get(k, 0))

# def solve_dict(aoc_input, part1=True, part2=True) :
#     lights_p1 = {}
#     lights_p2 = {}

#     for string in aoc_input.splitlines() :
#         if string == '' :
#             continue

#         instr, x1, y1, x2, y2 = re.match(r'(.*) (\d+),(\d+) through (\d+),(\d+)', string).groups()
#         #print (f'do {instr} for {x1},{y1} - {x2},{y2}')
#         switch_lights_dict(lights_p1, range(int(x1), int(x2)+1), range(int(y1), int(y2)+1), p1_func[instr])
#         switch_lights_dict(lights_p2, range(int(x1), int(x2)+1), range(int(y1), int(y2)+1), p2_func[instr])

#     return sum(lights_p1.values()), sum(lights_p2.values())

# #################
# # First solution, bit inefficient
# def switch_lights_solution1(lights, range_x, range_y, mode) :
#     '''either switch on (add to) or off (remove from) lights dict, or toggle.
#         param: ligths dict, x and y range, mode (turn on, turn off, toggle)
#         changes: lights'''
#     #print ('switch_lights: ', range_x, range_y, mode)
#     for x in range_x :
#         for y in range_y :
#             pos = (x, y)
#             k = key(pos)
#             if mode == 'turn on' :
#                 lights[k] = 1
#             elif mode == 'turn off' :
#                 if k in lights :
#                     del lights[k]
#             elif mode == 'toggle' :
#                 if k in lights :
#                     del lights[k]
#                 else :
#                     lights[k] = 1
#             else :
#                 exit (1)


# def tune_lights_solution1(lights, range_x, range_y, mode) :
#     '''either increase (add 1 to) or decreasse (remove 1 from) lights dict, or increase by 2 if toggle.
#         param: ligths dict, x and y range, mode (turn on, turn off, toggle)
#         changes: lights'''
#     for x in range_x :
#         for y in range_y :
#             pos = (x, y)
#             k = key(pos)
#             if mode == 'turn on' :
#                 lights[k] = lights.get(k, 0) + 1
#             elif mode == 'turn off' :
#                 if k in lights and lights[k] > 0 :
#                     lights[k] -= 1
#             elif mode == 'toggle' :
#                 lights[k] = lights.get(k, 0) + 2
#             else :
#                 exit (1)