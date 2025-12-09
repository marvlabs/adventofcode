#!python3
'''AoC 2025 Day 02'''
# from pprint import pprint as pp
import math
#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '02',
    'url'           :   'https://adventofcode.com/2025/day/02',
    'name'          :   "Day 2: Gift Shop - find patterns in numbers",
    'difficulty'    :   'D2',
    'learned'       :   'math vs string manipulation?',
    't_used'        :   '30',
    'result_p1'     :   16793817782,
    'result_p2'     :   27469417404,
}
#############
TESTS = [
 {
        'name'  : 'test',
        'input' : '''11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124''',
        'p1' : 1227775554,
        'p2' : 4174379265,
    },
]
#################
count_digits = lambda n: 1 if n == 0 else math.floor(math.log10(n)) + 1

def sum_doubled(rng) :
    start, end = map(int, rng.split('-'))
    sum = 0
    lowdigits = count_digits(start)
    highdigits = count_digits(end)

    for digits in range(lowdigits, highdigits+1) :
        if digits % 2 != 0 : continue  # must be even number of digits, otherwise no pairs

        lower = max(start, 10**(digits-1))
        upper = min(end, 10**digits - 1)

        for first_half in range(lower // (10**(digits//2)), (upper // (10**(digits//2))) + 1) :
            full_number = first_half * 10**(digits//2) + first_half # construct the full number by appending the first half to itself
            if full_number < lower or full_number > upper : continue
            #print(f'    found double: {full_number}')
            sum += full_number
    
    return sum

def sum_nd(rng) :
    start, end = map(int, rng.split('-'))
    sum = 0

    seen = set()
    lowdigits = count_digits(start)
    highdigits = count_digits(end)

    for digits in range(lowdigits, highdigits+1) :
        lower = max(start, 10**(digits-1))
        upper = min(end, 10**digits - 1)
        #print(f'  checking {lower}-{upper} with {digits} digits')

        for n in range(1, digits//2 + 1) :
            if digits % n != 0 : continue  # digits must be multiple of n

            for first_part in range(lower // (10**(digits - n)), (upper // (10**(digits - n))) + 1) :
                full_number = int(str(first_part) * (digits // n)) # this time, as string multiply :)
                if full_number < lower or full_number > upper : continue
                #print(f'    found n\'d: {full_number}')
                if full_number in seen : continue # This time: a number can match for several n, but must only be counted once
                seen.add(full_number)
                sum += full_number

    return sum


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0
    ranges = aoc_input.split(',')
    #print("checking how many numbers if brute forced:", sum(b-a for a,b in (map(int, rng.split('-')) for rng in ranges))) # Could have bruted it...
    for r in ranges :
        p1_result += sum_doubled(r)
        p2_result += sum_nd(r)
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
