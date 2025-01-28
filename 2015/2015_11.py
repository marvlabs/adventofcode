#!python3
'''AoC 2015 Day 11'''
import re
from itertools import groupby
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '11',
    'url'           :   'https://adventofcode.com/2015/day/11',
    'name'          :   "Corporate Policy - Password rules",
    'difficulty'    :   'D2',
    'learned'       :   'Python map list set lambda',
    't_used'        :   '60',
    'result_p1'     :   'cqjxxyzz',
    'result_p2'     :   'cqkaabcc',
}
#############
TESTS = [
 {
        'name'  : 'password-1',
        'input' : 'abcdefgh',
        'p1' : 'abcdffaa',
        'p2' : 'abcdffbb',
    },
 {
        'name'  : 'password-2',
        'input' : 'ghijklmn',
        'p1' : 'ghjaabcc',
        'p2' : 'ghjbbcdd',
    },
]
#################
def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''
    p1_result = find_next_pw(aoc_input)
    p2_result = find_next_pw(p1_result)
    return p1_result, p2_result


def find_next_pw(old_pw):
    '''Dumbly increment and test PW until one fits. 
    This should really be optimised to shortcut the increment on known failures, 
    i.e. it doesn't make sense to test all pw's starting from "i..." as they will all fail and can be bypassed by a smarter inc function.
    Turns out, it isn't necessary as it finds the solutions in about a second (1.2E6 pw's checked) (Test-2: 9s 8E6).'''
    nr_pws = 0
    new_pw = old_pw
    while True :
        nr_pws += 1
        if nr_pws % 1000000 == 0 : print (nr_pws, end=' ', flush=True)
        pw_good = True
        new_pw = increment_password(new_pw)
        for f_req in REQUIREMENTS :
            if not f_req(new_pw) : 
                pw_good = False
                break
        if pw_good :
            break
    print ('find_next_pw checked:', nr_pws)
    return new_pw


next_char = lambda c : 'a' if c == 'z' else chr(ord(c)+1)
def increment_password(old_pw) :
    '''Return next higher string'''
    incremented = False
    new_pw = ''
    for c in reversed(old_pw) :
        new_c = c if incremented else next_char(c)
        if not incremented and new_c != 'a' :
            incremented = True
        new_pw = new_c + new_pw
    return new_pw

#############
# PW requirments function list:
THREES = list(map(lambda ci : ''.join(map(chr, range(ci, ci+3)))  , range(ord('a'), ord(('y'))) ))
def req_straight_three (pw) :
    '''Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. 
    They cannot skip letters; abd doesn't count.'''
    for three in THREES :
        if three in pw : return True
    return False

def req_no_iol(pw) :
    '''Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.'''
    return not re.search(r'[iol]', pw)

def req_double_pair(pw) :
    '''Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.'''
    return len (list(filter(lambda g : len(g) > 1, set([''.join(group) for _, group in groupby(pw)])))) > 1

REQUIREMENTS = [ req_straight_three, req_no_iol, req_double_pair ]
#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    assert next_char('a') == 'b'
    assert next_char('z') == 'a'
    assert increment_password('xx') == 'xy'
    assert increment_password('xz') == 'ya'
    assert THREES[0] == ('abc')
    assert THREES[-1] == ('xyz')
    assert req_straight_three('hijklmmn')
    assert not req_straight_three('abbceffg')
    assert not req_no_iol('hijklmmn')
    assert not req_no_iol('abcdefgi')
    assert req_double_pair('abbceffg')
    assert not req_double_pair('abbcegjk')
    assert not req_double_pair('abbcegbb')

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
