#!python3
'''AoC 2015 Day 10'''
from itertools import groupby
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '10',
    'url'           :   'https://adventofcode.com/2015/day/10',
    'name'          :   "Elves Look, Elves Say - Say the Sequence",
    'difficulty'    :   'D1',
    'learned'       :   'groupby',
    't_used'        :   '15',
    'result_p1'     :   360154,
    'result_p2'     :   5103798,
}
#############
TESTS = [
]
#################
# My version - iterative, but faster
def say_sequence_coded(string) :
    '''Implement the "look and say" - say it as you read and count it -> next item'''
    count = 0
    result = ''
    cur = string[0]
    for c in string :
        if c != cur :
            result += str(count)
            result += cur
            cur = c
            count = 1
        else :
            count += 1
    result += str(count)
    result += cur
    return result


# The concise 'python-way' version: use group by / len / join
def say_sequence_groupby(string):
    '''Using groupby to split into consecutive-items lists, then add together again'''
    # This is more readable but a bit slower than the below (list conversion and len vs list comprehension for the counting of the grouped list)
    return ''.join(str(len(list(group))) + key for key, group in groupby(string))
    # return ''.join(str(len([1 for _ in v])) + k for k, v in groupby(string))


def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''

    string = aoc_input
    for i in range(40) :
        string = say_sequence_coded(string)
    p1_result = len(string)
    
    for i in range(10) :
        string = say_sequence_coded(string)
    p2_result = len(string)
    
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    assert say_sequence('1') == '11'
    assert say_sequence('11') == '21'
    assert say_sequence('21') == '1211'
    assert say_sequence('1211') == '111221'
    assert say_sequence('111221') == '312211'

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
