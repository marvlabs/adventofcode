#!python3
'''AoC 2016 Day 11'''
import re
from itertools import combinations, chain
from copy import deepcopy
from heapq import heappush, heappop
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '11',
    'url'           :   'https://adventofcode.com/2016/day/11',
    'name'          :   "Radioisotope Thermoelectric Generators - radiation risk",
    'difficulty'    :   'D3',
    'learned'       :   'This took multiply tries for the perfect result',
    't_used'        :   '240',
    'result_p1'     :   47, 
    'result_p2'     :   71,
}
#############
TESTS = [
{
    'name'  : '4-floors',
    'input' : '''The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.''',
    'p1' : None,#11,
    'p2' : None,
},
]
#################

# How much cumulated distance are all items from 4th floor -> 0 if all items are on the top floor
distance = lambda locations : sum( 8-m[0]-m[1] for m in locations.values() )

# A hash of a certain elevator position and item-on-floor distribution, used to check whether this situation has already been seen.
# The big optimization here: sorting of the generator/chip pairs over all materials.
# The theory being: it doesn't matter whether we have itemX/genX on floorA/floorB or itemY/genY on the same floorA/floorB
# These are 'the same situations' from a solving point of view. We don't need to play through both these options as it's going to lead to the same result
# This brings the nr of seen positions for p2 from 3E6 down to less than 8E3 (runtime 260s -> 0.7s)
situation_key = lambda materials, e : (e, tuple( (m[0], m[1]) for m in sorted(materials.values())))

# A* search: BFS optimized by prioritising the unvisited queue with current cost and 'distance' of all items from target position
def a_star(materials) :
    elevator = 1
    counter = 0
    seen = set()
    unvisited = []
    heappush(unvisited, (distance(materials), counter, 0, materials, elevator))
    seen.add(situation_key(materials, elevator))

    while len(unvisited) :
        _, _, cost, situation, elevator = heappop(unvisited)

        for next_situation, next_elevator in possible_situations(situation, elevator) :
            sk = situation_key(next_situation, next_elevator)
            if sk in seen : continue
            seen.add(sk)

            if distance(next_situation) == 0 :
                # print (f"Found end position after {counter} checks. Seen {len(seen)}, unvisited {len(unvisited)}")
                return cost+1 # Found end situation

            counter += 1 # Acts as tie breaker in the heap
            heappush(unvisited, (distance(next_situation)+cost+1, counter, cost+1, next_situation, next_elevator))

    return None


# From a current item-over-floor distribution and elevator position, get all valid next distributions after shuttling one or two items up or down according to the rules
def possible_situations(situation, elevator) :
    possible = []
    gens_on_floor = [ 'g_'+material for material in situation if situation[material][0] == elevator ]
    chips_on_floor = [ 'm_'+material for material in situation if situation[material][1] == elevator ]
    # List of all one- and two-combinations of all items on this floor
    combos = list(chain ( combinations(gens_on_floor + chips_on_floor, 2), [ ( item, None) for item in (gens_on_floor + chips_on_floor) ] ))

    for e in [ elevator + 1, elevator - 1 ] :
        if e < 1 or e > 4 : continue

        # Check resulting distributions for all combos when brought up or down one level
        for combo in combos:
            if not combo_valid(combo) : continue
            if combo[0] and combo[1] and e<elevator : continue # Optimized: don't bring down two items. Ever.
            
            new_situation = deepcopy(situation)
            for c in combo :
                if not c : continue
                if c[0] == 'g' : 
                    # move a generator to the new floor...
                    new_situation[c[2:]][0] = e
                else :
                    # move a chip to the new floor...
                    new_situation[c[2:]][1] = e
            # ... and check whether this results in a valid distribution
            if situation_valid(new_situation) :
                possible.append((new_situation, e))

    return possible


# Is this distribution of items on the floors allowed?
def situation_valid(situation) :
    for m_check in situation.values():
        if m_check[0] != m_check[1] :          
            # This Chip and Generator are not on the same floor: No other Generator allowed on the floor of this Chip
            for m_other in situation.values() :
                if m_other[0] == m_check[1] :
                    return False   # This generator is on the same floor as our unprotected chip
    return True


# Can this combination of 1 or 2 items go on an elevator?
def combo_valid(combo) :
    if (combo[0] == None) and (combo[1] == None) : return False  # Empty elevator not allowed
    if (combo[0] == None)  ^  (combo[1] == None) : return True   # Only one item, ok
    if combo[0][0] == combo[1][0]  : return True                 # Generator and Chip of the same material, ok
    return combo[0][1:] == combo[1][1:]                          # Generator and Chip of differing material are not allowed

##########################
def solve(aoc_input, part1=True, part2=True, attr=None) :
    item_locations = {}

    floor = 0
    for line in aoc_input.splitlines() :
        floor += 1
        for generator in re.findall(r'(\w+) generator', line) :
            item_locations.setdefault(generator, [None,None])[0] = floor
        for chip in re.findall(r'(\w+)-compatible microchip', line) :
            item_locations.setdefault(chip, [None,None])[1] = floor
    #print(sorted(materials.values())) # Can be used as seen key, can be used to compute distance

    # The counting solution: Works for my input, but NOT for the test input. REVISIT THIS!!!
    #p1_result = simple_counting_approach2(materials)
    #p2_result = simple_counting_approach2(materials)

    # FINALLY: realised a search with good key and optimaziation to find a path through all possible moves
    p1_result = a_star(item_locations)

    item_locations['elerium'] = [1,1]
    item_locations['dilithium'] = [1,1]
    p2_result = a_star(item_locations)

    return p1_result, p2_result

##########################
# The counting solution:
# Every item needs two steps to carry up one level, because:
# - Two up, one down : REPEAT -> this ferries the items up: two items, four moves.
# The last two don't use four, but only one: -> minus three
# This is an optimistic minimal result. If we need to shuffle around some rule infraction, this won't find it...
# NEEDS TO BE REVISITED -> While it gives the correct result for my input, id DOES NOT WORK for the test input
def simple_counting_approach(situation):
    moves = 0
    to_move = 0
    for floor in range(1,4) :
        to_move += sum(1 for m in situation.values() if m[0] == floor) + sum(1 for m in situation.values() if m[1] == floor)
        moves += 2*to_move - 3
    return moves
##########################

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
