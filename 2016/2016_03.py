#!python3
'''AoC 2016 Day 03'''
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '03',
    'url'           :   'https://adventofcode.com/2016/day/03',
    'name'          :   "Squares With Three Sides - triangle validation",
    'difficulty'    :   'D1',
    'learned'       :   'lists lists lists',
    't_used'        :   '15',
    'result_p1'     :   1032, 
    'result_p2'     :   1838,
}
#############
TESTS = [
{
        'name'  : 't-1-of-2',
        'input' : '''5 10 25
5 10 12
7 12 50''',
        'p1' : 1,
        'p2' : 2,
},
{
        'name'  : 't-threes',
        'input' : '''101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603''',
        'p1' : 3,
        'p2' : 6,
},]

#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = 0
    lines = aoc_input.splitlines()

    p1_result = sum([ s1 + s2 > s3 for s1, s2, s3 in [ sorted(map(int,l.split())) for l in lines ] ])
    
    for i in range(0, len(lines), 3) :
        l1 = list(map(int, lines[i].split()))
        l2 = list(map(int, lines[i+1].split()))
        l3 = list(map(int, lines[i+2].split()))
        for j in range(3) :
            s1, s2, s3 = sorted([l1[j], l2[j], l3[j]])
            if s1 + s2 > s3 : p2_result += 1

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
