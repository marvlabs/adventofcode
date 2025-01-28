#!python3
'''AoC 2024 Day 22'''
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '22',
    'url'           :   'https://adventofcode.com/2024/day/22',
    'name'          :   "Monkey Market: Going Bananas",
    'difficulty'    :   'D2',
    'learned'       :   'PLEASE don\'t brute force THE WHOLE range!',
    't_used'        :   '120',
    'result_p1'     :   14691757043,
    'result_p2'     :   1831,
}
#############
TESTS = [
{
'name'  : 'Secrets',
'input' : '''1
10
100
2024''',
'p1' : 37327623,
'p2' : None,
},

{
'name'  : 'Changes',
'input' : '''1
2
3
2024''',
'p1' : None,
'p2' : 23, # seq === [-2,1,-1,3]
},

]

#################

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0
    monkeys = [ int(init) for init in aoc_input.splitlines() ]

    for init in monkeys :
        p1_result += find_nth(init, 2000)

    p2_result = find_best_change(monkeys)

    return p1_result, p2_result


# Compute all possible patterns for each monkey and add sum to the pattern list
def find_best_change(monkeys) :
    patterns = {}
    for m in monkeys :
        all_patterns(m, patterns)
    return max(patterns.values())


pkey = lambda l : tuple(l)
secret_cost = lambda s: s%10

# Compute all patterns in the price list for a start value, store the cumulated price for each pattern in a dict
# This is WAY less than to check all possible permuations
def all_patterns(secret, all_patterns) :
    monkey_patterns = {}

    price_list = [ secret_cost(secret) ]
    for i in range(0, 2000) :
        secret = next_nr(secret)
        price_list.append(secret_cost(secret))
    
    for i in range(0, 2000-4) :
        next_five = price_list[i:i+5] 

        pattern_key = pkey( [ next_five[j+1] - next_five[j] for j in range(len(next_five)-1) ] ) 
        if pattern_key not in monkey_patterns : # Only use the price of the first occurence of a pattern
            monkey_patterns[pattern_key] = next_five[-1]
            all_patterns[pattern_key] = all_patterns.get(pattern_key, 0) + next_five[-1]
    return



def find_nth(init, n) :
    next = init
    for i in range(n) :
        next = next_nr(next)
    return next

#mix_prune  = lambda s, x : (s ^ x) % 16777216
# def next_nr(nr) :
#     next = mix_prune(nr, nr*64)
#     next = mix_prune(next, next // 32)
#     next = mix_prune(next, next * 2048)
#     return next

def next_nr(s) :
    s = (s ^ s << 6) & 0xFFFFFF
    s = (s ^ s >> 5) & 0xFFFFFF
    return (s ^ s << 11) & 0xFFFFFF

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    assert next_nr(123) == 15887950
    assert find_nth(123, 1) == 15887950
    assert find_nth(123, 10) == 5908254

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
