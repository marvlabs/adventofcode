#!python3
'''AoC 2025 Day 05'''
#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '05',
    'url'           :   'https://adventofcode.com/2025/day/05',
    'name'          :   "Day 5: Cafeteria - food ranges",
    'difficulty'    :   'D2',
    'learned'       :   'ranges - again; and list comprehension - again',
    't_used'        :   '15',
    'result_p1'     :   789,
    'result_p2'     :   343329651880509,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''3-5
10-14
16-20
12-18

1
5
8
11
17
32
''',
        'p1' : 3,
        'p2' : 14,
    },
]
#################
def add_ranges(ranges) :
    '''Merge overlapping and adjacent ranges and add their lengths on the go'''
    sorted_ranges = sorted(ranges, key=lambda r: r[0])
    sum_ranges = 0

    current_range = sorted_ranges[0]
    for next_range in sorted_ranges[1:]:
        if next_range[0] <= current_range[1] + 1:  # Overlapping or adjacent, merge into current range
            current_range = (current_range[0], max(current_range[1], next_range[1]))
        else:
            sum_ranges += current_range[1] - current_range[0] + 1
            current_range = next_range

    return sum_ranges + current_range[1] - current_range[0] + 1


def solve(aoc_input, part1=True, part2=True, attr=None) :
    puzzle_parts = aoc_input.split("\n\n")
    ranges = [ tuple(map(int, line.split('-'))) for line in puzzle_parts[0].splitlines() ]
    foods = map(int, puzzle_parts[1].splitlines())

    p1_result = sum( 1 for food in foods if any( r[0] <= food <= r[1] for r in ranges ) )
    p2_result = add_ranges(ranges)

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
