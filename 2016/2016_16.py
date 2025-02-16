#!python3
'''AoC 2016 Day 16'''
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '16',
    'url'           :   'https://adventofcode.com/2016/day/16',
    'name'          :   "Dragon Checksum - fill that disk",
    'difficulty'    :   'D1',
    'learned'       :   'String reverse slice',
    't_used'        :   '15',
    'result_p1'     :   '11101010111100010', 
    'result_p2'     :   '01001101001000101',
}
#############
TESTS = [
{
    'name'  : 'dragon-20',
    'input' : '''10000''',
    'p1' : '01100',
    'p2' : None,
    'testattr' : 20,
},
]

#################

def dragon_expand(seed, target_len) :
    while len(seed) < target_len :
        seed = seed + '0' + seed[::-1].replace('0', 'x').replace('1', '0').replace('x', '1')
    return seed

def checksum(data) :
    while len(data) % 2 == 0 :
        data = ''.join('1' if data[i] == data[i+1] else '0' for i in range(0, len(data), 2))
    return data

assert dragon_expand('111100001010', 20) == '1111000010100101011110000'
assert checksum('110010110100') == '100'

def solve(aoc_input, part1=True, part2=True, attr=None) :
    init = aoc_input.strip()
    disk_len = 272 if not attr else attr
    p1_result = checksum(dragon_expand(init, disk_len)[:disk_len])
    disk_len = 35651584 if not attr else attr
    p2_result = checksum(dragon_expand(init, disk_len)[:disk_len])

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
