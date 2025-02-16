#!python3
'''AoC 2016 Day 19'''
from math import log
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '19',
    'url'           :   'https://adventofcode.com/2016/day/19',
    'name'          :   "An Elephant Named Joseph - remove elves from circle",
    'difficulty'    :   'D3',
    'learned'       :   'list removal is expenisve - just point around',
    't_used'        :   '150',
    'result_p1'     :   1834471, 
    'result_p2'     :   1420064,
}
#############
TESTS = [
{
    'name'  : 'circle-5',
    'input' : '''5''',
    'p1' : 3,
    'p2' : 2,
},

{
    'name'  : 'circle-10',
    'input' : '''10''',
    'p1' : 5,
    'p2' : 1,
},
{
    'name'  : 'circle-11',
    'input' : '''11''',
    'p1' : 7,
    'p2' : 2,
},
]

#################

# Create an elf circle. Index is number, value is the next elf's idx
# Elves [idx] points to the next elf. To remove one from the chain, just point past it
def link_elves(nr_of_elves) :
    elves = [ None ]
    for e in range(1, nr_of_elves+1) :
        elves.append(e+1)
    elves[-1] = 1
    return elves


def steal_next(nr_of_elves):
    elves = link_elves(nr_of_elves)
    current_elf = 1

    # Remove the next in line, go the new next, repeat until all but one removed
    while current_elf != elves[current_elf] :
        #robbed_elf = elves[current_elf]
        elves[current_elf] = elves[elves[current_elf]]
        current_elf = elves[current_elf]
        #elves[robbed_elf] = None # Just for clarity in the list, not needed

    return current_elf

# Optimization was needed for p2:
# - I first did a list removal version for P1. It worked, not too fast, but WAY too expensive for P2 -> I let this version actually run for P2, and it finished after exactly one day with the correct result :-)
# - single linked list works if the next can be circumvented, see p1 above, but:
# - skipping ahead half around the circle to the robbed elf every time is still too expensive
# -> after finding the first elf to rob, we keep track of the the poor bastards: it's the next, then one skipped, then the next again
#    This saves the the scanning through the list every time
# (Actually, we keep track of the one before the poor bastards, as we need to change this elves pointer)
def steal_opposite(nr_of_elves):
    elves = link_elves(nr_of_elves)
    current_elf = 1
    linked_elves = nr_of_elves

    # Find the elf before the first elf to be robbed. Skip around half the circle the first time
    elf_before_next_robbed = current_elf
    advance = (linked_elves // 2) - 1
    for _ in range(advance) :
        elf_before_next_robbed = elves[elf_before_next_robbed]

    while linked_elves > 1 :
        robbed_elf = elves[elf_before_next_robbed]
        elf_before_robbed = elf_before_next_robbed

        if linked_elves % 2 == 1 :
            # Only advance if we need to skip the next elf. If not, it's advanced by removing the robbed elf anyways
            elf_before_next_robbed = elves[robbed_elf]

        new_next_elf = elves[robbed_elf]
        elves[elf_before_robbed] = new_next_elf
        elves[robbed_elf] = None # Just for the clarity in the list

        current_elf = elves[current_elf]
        linked_elves -= 1
    
    return current_elf


# After the fact:
# Turns out that P1 is the Josephus Problem. VERY Good explanation: https://www.youtube.com/watch?v=uCsD3ZGzMgE
# From this, we have a rather easy alternative solution
def josephus(n):
    return int(f'{n:b}'[1:]+'1', 2)

# Simulating P2 for some numbers ...
#for i in range(2, 200) :
#    print(i, steal_next(i), steal_opposite(i))
# ...also shows a pattern, something like:
# 3^x + (n-3^x) for 3^x < n  and n < 2*3^x , and double the diff for 3^x < n and n > 2*3^x, or better put:
# "The sequence is N when N is power of 3, otherwise it goes up by 1 from N - 3^floor(log3(N)) for the next 3^floor(log3(N)) and then goes up by two"
def not_josephus(n):
    exp3 = int(log(n-1, 3))
    result = n - 3**exp3
    if result > 3**exp3 : 
        result += result - 3**exp3
    return result


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = 0
    nr_of_elves = int(aoc_input.strip())

    p1_result = steal_next(nr_of_elves)
    assert p1_result == josephus(nr_of_elves)
    
    p2_result = steal_opposite(nr_of_elves)
    assert p2_result == not_josephus(nr_of_elves)
    
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
