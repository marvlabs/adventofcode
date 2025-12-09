#!python3
'''AoC 2025 Day 09'''
from grid import Grid
import anim
#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '09',
    'url'           :   'https://adventofcode.com/2025/day/09',
    'name'          :   "Day 9: Movie Theater - is your square in shape?",
    'difficulty'    :   'D3',
    'learned'       :   'Details, lines, boundaries... aaarghhh',
    't_used'        :   '120',
    'result_p1'     :   4755278336,
    'result_p2'     :   1534043700,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
''',
        'p1' : 50,
        'p2' : 24,
    },
]
#################

is_vertical   = lambda line : line[0][0] == line[1][0]
is_horizontal = lambda line : line[0][1] == line[1][1]

# Return the lines inside a square, inner borders. These cannot touch a bounding line and are therefore interesting
# (As we only check large squares, we do not care about 'flattened' squares without a real inside)
# Note: try with fractions maybe?
def inner_sides(square) :
    s = []
    xmin = min(square[0][0], square[1][0])
    ymin = min(square[0][1], square[1][1])
    xmax = max(square[0][0], square[1][0])
    ymax = max(square[0][1], square[1][1])

    corner_1 = (xmin+1, ymin+1)
    for corner_2 in  (xmax-1, ymin+1), (xmax-1, ymax-1), (xmin+1, ymax-1), (xmin+1, ymin+1) :
        s.append((corner_1, corner_2))
        corner_1 = corner_2
    return s


# A point is sitting on a boundary line
def on_boundary(point, bounding_lines) :
    for l in bounding_lines :
        if on_line(point, l) : return True

# A point is part of a line
def on_line(point, line) :
    if is_vertical(line)   : 
        return (
            point[0] == line[0][0] and
            min(line[0][1], line[1][1]) <= point[1] <= max(line[0][1], line[1][1])
        )
    else :
        return (
            point[1] == line[0][1] and
            min(line[0][0], line[1][0]) <= point[0] <= max(line[0][0], line[1][0])
        )

# Either a corner is on the boundary, or it does cross an odd number of boundary lines to reach the outside
def corners_are_inside(square, bounding_lines) :
    # Only check the non-red corners - the red ones are inside by definitioin
    for corner in  (square[1][0], square[0][1]), (square[0][0], square[1][1]):
        if on_boundary(corner, bounding_lines) : continue
        
        # Attention: Different case for U-bend vs S-bend. Dealt with by offsetting 0.1 to miss the U-Bend or have 2 hits, while S-bend will always have 1 hit
        if intersect_line(((corner[0]+0.1, corner[1]+0.1), (0.1,corner[1]+0.1)), bounding_lines) %2 == 0 : return False
    
    return True


def intersect_square_boundary(square, bounding_lines) :
    # no boundary may touch the inside of the square
    for side in inner_sides(square) :
        if intersect_line(side, bounding_lines) : 
            return True
    return False

def intersect_line(line, bounding_lines) :
    for l in bounding_lines :
        if intersect(line, l) : 
            return True
    return False


def intersect(line1, line2) :
    if is_vertical(line1)   and is_vertical(line2)  : return False # both are vertical
    if is_horizontal(line1) and is_horizontal(line2): return False # both are horizontal 

    if is_vertical(line1) :
        return ( ((line2[0][0] <= line1[0][0] <= line2[1][0]) or (line2[1][0] <= line1[0][0] <= line2[0][0]))
            and  ((line1[0][1] <= line2[0][1] <= line1[1][1]) or (line1[1][1] <= line2[0][1] <= line1[0][1])) )
    else :
        return ( ((line2[0][1] <= line1[0][1] <= line2[1][1]) or (line2[1][1] <= line1[0][1] <= line2[0][1]))
            and  ((line1[0][0] <= line2[0][0] <= line1[1][0]) or (line1[1][0] <= line2[0][0] <= line1[0][0])) )


def solve(aoc_input, part1=True, part2=True, attr=None) :
    reds = [ tuple(map(int, line.split(','))) for line in aoc_input.splitlines() if line.strip() != '' ]

    g = Grid(200,200, '.')
    a = anim.AnimGrid(anim.Screen(1000,1050, 'Movie Theater'), g.dim_x, g.dim_y, use_chars=False, status_area=50, 
        title='AOC 2025 DAY 9 - Movie Theater', movie = "AOC_2025-09_Movie_Theater")
    a.color_map = { '.': 'DARK_GRAY', '@': 'BLUE', '#': 'RED', 'X': 'GREEN', 'default': 'BLACK' }

    a.draw(g, 500, f'finding red tiles...')

    squares = {}
    frame = 0
    for i in range(len(reds)) :
        g.set((reds[i][0]//500,reds[i][1]//500), '#')
        frame += 1
        if frame % 50 == 0 : a.draw(g, 5, f'Red Tiles {frame}')
        
        for j in range(i+1, len(reds)) :
            squares[(reds[i], reds[j])] = (abs(reds[i][0]-reds[j][0])+1) * (abs(reds[i][1]-reds[j][1])+1)
    p1_result = max(squares.values())

    a.draw(g, 300, f'Red Tiles:  {frame}')
    #print(g)

    reds.append(reds[0])
    bounding_lines = [ ((reds[i][0], reds[i][1]), (reds[i+1][0], reds[i+1][1])) for i in range(len(reds)-1)]

    frame = 0
    for line in bounding_lines :
        frame += 1
        g.line((line[0][0]//500, line[0][1]//500), (line[1][0]//500, line[1][1]//500), 'X')
        if frame % 10 == 0 : a.draw(g, 5, f'checking boundary... {frame}')

    a.draw(g, 300, f'Boundaries: {len(bounding_lines)}  ')
    frame = 0
    for square in sorted(squares.items(), key=lambda item: item[1], reverse=True) :
        frame += 1
        if frame % 200 == 0 :
            g_back = g.copy()
            for side in inner_sides(square[0]) :
                g.line((side[0][0]//500, side[0][1]//500), (side[1][0]//500, side[1][1]//500), '@')
            a.draw(g, 25, f'checking squares... {frame}')
            g = g_back
        if not intersect_square_boundary(square[0], bounding_lines) and corners_are_inside(square[0], bounding_lines) : break 

    for side in inner_sides(square[0]) :
        g.line((side[0][0]//500, side[0][1]//500), (side[1][0]//500, side[1][1]//500), '@')
    a.draw(g, 3000, f'Largest Square: {square[0]} {square[1]}')
    a.save_movie(fps=25)

    p2_result = square[1]

    return p1_result, p2_result


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    #aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
