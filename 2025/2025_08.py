#!python3
'''AoC 2025 Day 08'''
from math import sqrt, prod

#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '08',
    'url'           :   'https://adventofcode.com/2025/day/08',
    'name'          :   "Day 8: Playground - wire up them boxes",
    'difficulty'    :   'D2',
    'learned'       :   'Why not just do it right the first time? Kruskal\'s algorithm',
    't_used'        :   '60',
    'result_p1'     :   105952,
    'result_p2'     :   975931446,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
''',
        'p1' : 40,
        'p2' : 25272,
        'testattr': 10,
    },
]
#################
dist_3d = lambda a,b : sqrt(abs(a[0]-b[0])**2 + abs(a[1]-b[1])**2 + abs(a[2]-b[2])**2)

# Compute all pairwise distances between boxes, do that only once and store in a dict
def all_diffs(boxes) :
    distances = {}
    for i in range(len(boxes)) :
        for j in range(i+1, len(boxes)) :
            distances[(i,j)] = dist_3d(boxes[i], boxes[j])
    return distances

# Merge all circuits that share boxes by repeated contraction until no more contractions are possible
def contract_circuits(circuits) :
    while contract_one(circuits) : pass

def contract_one(circuits) :
    for i in range(len(circuits)) :
        for j in range(i+1, len(circuits)) :
            if circuits[i].intersection(circuits[j]) :
                circuits[i].update(circuits[j])
                del circuits[j]
                return True
    return False

# This is only an optimization, we could just do the append instead of addint to existing circuits.
# The contraction would sort it out, but would have more work to do (2.5 times slower)
def plug_next_connection(closest, circuits) :
    for c in circuits :
        if closest[0] in c or closest[1] in c :
            c.update({closest[0], closest[1]})
            return
    circuits.append({closest[0], closest[1]})


def solve(aoc_input, part1=True, part2=True, attr=None) :
    rounds = attr if attr else 1000 # less rounds for test input
    boxes = [ list(map(int, line.split(','))) for line in aoc_input.splitlines() if line.strip() != '' ]
    sorted_distances = sorted(all_diffs(boxes).items(), key=lambda item: item[1])
    circuits = []

    # Part 1 : Wire up the first n closest connections
    for round in range(rounds) :
        closest = sorted_distances[round][0]
        plug_next_connection(closest, circuits)
    contract_circuits(circuits)
    p1_result = prod(sorted([ len(c) for c in circuits ])[-3:])

    # Part 2 : Continue wiring until the one and only last circuit contains all boxes
    while len(circuits[0]) < len(boxes) :
        round += 1
        closest = sorted_distances[round][0]
        plug_next_connection(closest, circuits)
        contract_circuits(circuits)
    p2_result = boxes[closest[0]][0] * boxes[closest[1]][0]  

    return p1_result, p2_result


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
