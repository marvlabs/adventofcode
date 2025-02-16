#!python3
'''AoC 2016 Day 21'''
import re
from itertools import permutations
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '21',
    'url'           :   'https://adventofcode.com/2016/day/21',
    'name'          :   "Scrambled Letters and Hash - lots of instructions",
    'difficulty'    :   'D2',
    'learned'       :   'Good design pays off?',
    't_used'        :   '60',
    'result_p1'     :   'agcebfdh', 
    'result_p2'     :   'afhdbegc',
}
#############
TESTS = [
{
    'name'  : 'scramble / unscramble',
    'input' : '''swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d''',
    'p1' : 'decab',
    'p2' : 'abcde',
    'testattr' : '''abcde''',
},
]
#################
# Instructions:
# swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
# swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in the string).
# rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
# rotate based on position of letter X means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
# reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
# move position X to position Y means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.
# -> implement all these as functions. 
# For P2: add a reverse flag to 'undo' the operations. Some need nothing, one needs a BF search.
# Addendum: would have been quicker-and-dirtier to just BF the whole backwards thingy?
# Let's see here:
def bf_reverse(instructions, scrambled) :
    pws = list()
    for pw in [ ''.join(p) for p in permutations(scrambled) ]:
        if run_instructions(instructions, pw) == scrambled : 
            pws.append(pw)
    return pws[-1]
# -> It works and takes 3.5s. BUT it fails on the test input, because there's more than one possible solution. Shitty Scrambling!
# Generating all of them instead of retuning the first found: it's the second one which is correct for the test.

# All scramble functions:
def swap_position(pw, instruction, rev=False) :
    x, y = sorted(map(int, re.findall(r'\d+', instruction)))
    return pw[:x] + pw[y:y+1] + pw[x+1:y] + pw[x:x+1] + pw[y+1:]

def swap_letter(pw, instruction, rev=False) :
    a, b = re.findall(r'\s(\w)\s', instruction+' ')
    return pw.replace(a, '^').replace(b, a).replace('^', b)

def rotate_left(pw, instruction, rev=False) : 
    if rev : return rotate_right(pw, instruction)
    x = int(re.findall(r'\d+', instruction)[0])  % len(pw)
    return pw[x:] + pw[:x]

def rotate_right(pw, instruction, rev=False) :
    if rev : return rotate_left(pw, instruction) 
    x = int(re.findall(r'\d+', instruction)[0]) % len(pw)
    return pw[-x:] + pw[:-x]

def rotate_based(pw, instruction, rev=False) :
    if rev :
        # Brute force: Try all the possible backward rotations as input to find the one which produces the correct output
        for i in range(1, len(pw)+1) :
            test_pw = rotate_left(pw, f'rotate left {i} steps')
            if pw == rotate_based(test_pw, instruction) : 
                return test_pw
        else :
            return pw # None found!

    letter = instruction[-1]
    x = pw.find(letter)
    x += 2 if x >=4 else 1
    return rotate_right(pw, f'rotate right {x} steps')

def reverse_positions(pw, instruction, rev=False) :
    x, y = sorted(map(int, re.findall(r'\d+', instruction)))
    return pw[:x] + pw[x:y+1][::-1] + pw[y+1:]

def move_position(pw, instruction, rev=False) :
    x, y = map(int, re.findall(r'\d+', instruction))
    if rev:
        x, y = y, x
    letter = pw[x]
    remainder = pw[:x] + pw[x+1:]
    return remainder[:y] + letter + remainder[y:]


def run_instructions(instructions, pw, rev = False):
    for inst in instructions :
        func_name = '_'.join(inst.split()[0:2])
        pw = globals()[func_name](pw, inst, rev)
    return pw


def solve(aoc_input, part1=True, part2=True, attr=None) :
    instructions = aoc_input.splitlines()

    # Scramble
    pw = 'abcdefgh' if not attr else attr
    p1_result = run_instructions(instructions, pw)

    scrambled = 'fbgdceah' if not attr else p1_result
    p2_result = run_instructions(reversed(instructions), scrambled, rev=True)

    #p2_result = bf_reverse(instructions, scrambled) # Just for fun: brute force also works

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    assert swap_position('abcde', 'swap position 4 with position 0') == 'ebcda'
    assert swap_position('ebcda', 'swap position 4 with position 0', rev=True) == 'abcde'
    assert swap_letter('ebcda', 'swap letter d with letter b') == 'edcba'
    assert swap_letter('edcba', 'swap letter d with letter b', rev=True) == 'ebcda'
    assert rotate_left('edcba', 'rotate left 1 step') == 'dcbae'
    assert rotate_left('dcbae', 'rotate left 1 step', rev=True) == 'edcba'
    assert rotate_right('abcd', 'rotate right 1 step') == 'dabc'
    assert rotate_right('ecabd', 'rotate right 6 step') == 'decab'
    assert rotate_right('dabc', 'rotate right 1 step', rev=True) == 'abcd'
    assert rotate_right('decab', 'rotate right 6 step', rev=True) == 'ecabd'
    assert rotate_based('abdec', 'rotate based on position of letter b') == 'ecabd'
    assert rotate_based('ecabd', 'rotate based on position of letter b', rev=True) == 'abdec'
    assert reverse_positions('abcd', 'reverse positions 0 through 4') == 'dcba'
    assert reverse_positions('abcde', 'reverse positions 1 through 3') == 'adcbe'
    assert reverse_positions('adcbe', 'reverse positions 1 through 3', rev=True) == 'abcde'
    assert move_position('abcde', 'move position 1 to position 4') == 'acdeb'
    assert move_position('acdeb', 'move position 1 to position 4', rev=True) == 'abcde'

    # Main
    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
