#!python3
#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '05',
    'url'           :   'https://adventofcode.com/2015/day/5',
    'name'          :   "Doesn't He Have Intern-Elves For This? - Nice String",
    'difficulty'    :   'D1',
    'learned'       :   'Python loops, slice',
    't_used'        :   '45',
    'result_p1'     :   258,
    'result_p2'     :   53,
}
#############
TESTS = [
    {
        'name'  : 'nice-1',
        'input' : '''
ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
''',
        'p1' : 2,
        'p2' : None,
    },
    {
        'name'  : 'nice-2',
        'input' : '''
qjhvhtzxzqqjkmpb
xxyxx
uurcxstgmygtbstg
ieodomkazucvgmuy
''',
        'p1' : None,
        'p2' : 2,
    },
]
#############
# P1 rules
def check_vowels(s) :
    '''Check: It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.'''
    return  len([l for l in s if l in "aeiou"]) >= 3

def check_twice(s) :
    '''Check: It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).'''
    last_c = ''
    for c in s :
        if c == last_c :
            return True
        last_c = c
    return False

def check_no_bad(s) :
    '''Check: It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.'''
    for bad in ('ab', 'cd', 'pq', 'xy') :
        if (s.find(bad) >= 0) :
            return False
    return True

# P2 rules
def check_double_pair(s) :
    '''It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).'''
    for i in range(len(s) - 3) :
        if (s.find(s[i:i+2], i+2) > i) :
            return True
    return False

def check_repeat_separate(s) :
    '''It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.'''
    for i in range(len(s) - 2) :
        if (s[i:i+3][0] ==  s[i:i+3][2]) :
            return True
    return False


def find_nice_p1(aoc_input):
    nr_nice = 0
    for string in aoc_input.splitlines() :
        if string == '' :
            continue
        if (check_vowels(string)  and check_twice(string) and check_no_bad(string)) :
            nr_nice += 1
    return nr_nice


def find_nice_p2(aoc_input):
    nr_nice = 0
    for string in aoc_input.splitlines() :
        if string == '' :
            continue
        if (check_double_pair(string)  and check_repeat_separate(string)) :
            nr_nice += 1
    return nr_nice


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1 = find_nice_p1(aoc_input)
    p2 = find_nice_p2(aoc_input)
    return p1, p2


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    assert check_vowels('aei') == True
    assert check_vowels('xazegov') == True
    assert check_vowels('aeiouaeiouaeiou') == True
    assert check_twice('xx') == True
    assert check_twice('abcdde') == True
    assert check_twice('aabbccdd') == True
    assert check_no_bad('xcdx') == False
    assert check_double_pair('xyxy') == True
    assert check_double_pair('aabcdefgaa') == True
    assert check_double_pair('aaa') == False
    assert check_repeat_separate('xyx') == True
    assert check_repeat_separate('abcdefeghi') == True
    assert check_repeat_separate('aaa') == True

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
