#!python3
'''AoC 2024 Day 12'''
from grid import Grid, step
import anim

#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '12',
    'url'           :   'https://adventofcode.com/2024/day/12',
    'name'          :   "Garden Groups: fence them in",
    'difficulty'    :   'D3',
    'learned'       :   'find corners of a region',
    't_used'        :   '90',
    'result_p1'     :   1319878,
    'result_p2'     :   784982, #774471 too low
}
#############
TESTS = [



#     {
#         'name'  : 'G-DEBUG',
#         'input' : '''
# EEEA
# EEEA
# AAEA
# EAAA
# ''',
#         'p1' : 232,
#         'p2' : 80,
#     },
    
    {
        'name'  : 'G5',
        'input' : '''
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
''',
        'p1' : 772,
        'p2' : 436,
    },    
    
    {
        'name'  : 'G10',
        'input' : '''
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
''',
        'p1' : 1930,
        'p2' : 1206,
    },
    
    {
        'name'  : 'G-E',
        'input' : '''
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
''',
        'p1' : None,
        'p2' : 236,
    },
    
    {
        'name'  : 'G10',
        'input' : '''
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
''',
        'p1' : None,
        'p2' : 368,
    },
]
#################

def scan_region(g, pos, visited, region, perimeter) :
    plant = g.get(pos)
    region.append(pos)
    visited[pos] = True

    for dir, next_plant in g.neighbours90(pos).items() :
        next_pos = step(pos, dir)
        
        if not g.valid(next_pos) or plant != next_plant :
            # The neighbour plot is either out of bounds or has different plant -> This creates a border for our region here
            perimeter.append(next_pos)
            continue

        if next_pos in visited: continue

        # Recurse same region, different plot
        region, perimeter = scan_region(g, next_pos, visited, region, perimeter)

    return region, perimeter

def find_corners(area) :
    corners = 0
    for pos in area :
        # pos is a NE corner when 
        # - NE is not in the same area and both N and E are in the same area (internal corner)
        # - or N and E are not in the same area (external corner)
        for corner in ['NE', 'NW', 'SE', 'SW'] :
            dir1, dir2 = list(corner)
            if ((step(pos, corner) not in area) and (step(pos, dir1) in area) and (step(pos, dir2) in area))  \
                or ((step(pos, dir1) not in area) and (step(pos, dir2) not in area)) :
                corners += 1
    return corners

a = anim.AnimGrid(anim.Screen(140*8, 140*8, 'Garden, Regions, Plots'), 140, 140, use_chars=False)
anim.COLORS.update(anim.make_color_gradient('ry', 'RED', 'YELLOW', 26))
a.color_map.update( { chr(i+ord('A')) : 'ry_'+str(i) for i in range(26) } )

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = 0
    garden = Grid.from_string(aoc_input)
    a.draw(garden, 10000)
    visited = {}

    for pos in garden.all_pos() :
        if pos in visited : continue

        area, perimeter = scan_region(garden, pos, visited, region=[], perimeter=[])
        p1_result += len(area) * len(perimeter)

        lines = find_corners(area) # Nr of corners == Nr of Edges
        p2_result += len(area) * lines
    
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    #aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)


####
# My first attempt at finding edges by finding straight lines in all peripery fields
# It actually works with all test input but fails on the puzzle - which makes it really hard to debug
# It fails when a too long line is found because it snatches a periphery field not belonging to that line, but to one perpendicular to it.
# Then the one perpendicular is split into two.
# Could maybe made to work? But finding corners is much easier and clearer.

# lines = find_straight_lines(perimeter)

# def find_line(pos, perimeter, horizontal) :
#     line_length = 1
#     debug = False
#
#     dir_1 = 'W' if horizontal else 'S'
#     dir_2 = 'E' if horizontal else 'N'
#
#     for dir in [dir_1, dir_2] :
#         pos_next = step(pos, dir)
#         while pos_next in perimeter :
#             line_length += 1
#             perimeter.remove(pos_next)
#             pos_next = step(pos_next, dir)

# def find_straight_lines(perimeter) :
#     lines = 0
#     while len(perimeter) :
#         pos = perimeter.pop()
#         has_horizontal = find_line(pos, perimeter, horizontal=True)
#         if has_horizontal == 1 :
#             find_line(pos, perimeter, horizontal=False)
#         lines += 1
#     return lines
