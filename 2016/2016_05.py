#!python3
'''AoC 2016 Day 05'''
from hashlib import md5
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '05',
    'url'           :   'https://adventofcode.com/2016/day/05',
    'name'          :   "How About a Nice Game of Chess? - pw rules be crazy",
    'difficulty'    :   'D2',
    'learned'       :   'MD5 in Python',
    't_used'        :   '20',
    'result_p1'     :   '1a3099aa', 
    'result_p2'     :   '694190cd',
}
#############
TESTS = [
{
        'name'  : 'mdfive',
        'input' : '''abc''',
        'p1' : '18f47a30',
        'p2' : '05ace8e3',
},
]

#################

assert md5('abc3231929'.encode()).hexdigest()[:6] == '000001'
assert md5('abc3231929'.encode()).hexdigest()[:7] == '0000015'

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = ''
    p2_result = 'xxxxxxxx'

    i = 0
    while True:
        h = md5(f'{aoc_input}{i}'.encode())
        h_hex = h.hexdigest()
        
        if h_hex[:5] == '00000' :
            if len(p1_result) < 8 :
                p1_result += f'{h_hex[5]}'
            
            pos = int(h_hex[5], base=16)
            if pos < 8 and p2_result[pos] == 'x' :
                p2_result = p2_result[:pos] + h_hex[6] + p2_result[pos+1:]

            if len(p1_result) == 8 and 'x' not in p2_result : 
                print (f"Found both passwords with {i:_} tries")
                break

        i += 1



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
