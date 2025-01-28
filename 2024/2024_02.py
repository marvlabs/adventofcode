#!python3
'''AoC 2024 Day 02'''
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '02',
    'url'           :   'https://adventofcode.com/2024/day/02',
    'name'          :   "Red-Nosed Reports: does it rise or does it fall",
    'difficulty'    :   'D1',
    'learned'       :   'del',
    't_used'        :   '15',
    'result_p1'     :   442,
    'result_p2'     :   493,
}
#############
TESTS = [
 {
        'name'  : 'Test Report',
        'input' : '''
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
''',
        'p1' : 2,
        'p2' : 4,
    },
]
#################
def check_report(report) :
    direction = report[1] - report[0]
    direction = direction / abs(direction) if direction else 0

    for i in range(1, len(report)) :
        if not 1 <= (report[i] - report[i-1])*direction <= 3 : return 0
    return 1

def check_report_damped(report) :
    if check_report(report) : return 1

    for i in range(len(report)) :
        report_variation = report.copy()
        del report_variation[i]
        if check_report(report_variation) : return 1

    return 0



        
def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    p1_result, p2_result = 0, 0
    for string in aoc_input.splitlines()  :
        if string == '' : continue
        report = list(map(int, string.split()))
        p1_result += check_report(report)
        p2_result += check_report_damped(report)

        #print (report)
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
