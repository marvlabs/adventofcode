#!python3
'''AoC 2016 Day 07'''
import re
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '07',
    'url'           :   'https://adventofcode.com/2016/day/07',
    'name'          :   "Internet Protocol Version 7 - abababawhathteabba",
    'difficulty'    :   'D2',
    'learned'       :   'Look at the input. Twice.',
    't_used'        :   '30',
    'result_p1'     :   105,
    'result_p2'     :   258,
}
#############
TESTS = [
{
        'name'  : 'abba2',
        'input' : '''abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn''',
        'p1' : 2,
        'p2' : None,
},
{
        'name'  : 'bab3',
        'input' : '''aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb''',
        'p1' : None,
        'p2' : 3,
},]

#################
def has_abba(s) :
    for i in range(len(s)-3) :
        if s[i] == s[i+3] and s[i+1] == s[i+2] and s[i] != s[i+1] :
            return True
    return False
def is_tls(ip):
    if not has_abba(ip) : return 0
    for hypernet in re.findall(r'\[(.*?)\]', ip) :
        if has_abba(hypernet) : return 0
    return 1


# This is not 'clean': if a supernet matches a hypernet, it is filtered out of the all list. Doesn't matter for the result though...
def ip_parts(ip) :
    hypernets = re.findall(r'\[(.*?)\]', ip)
    all = re.findall(r'(\w+)', ip)
    return list(set(all) - set(hypernets)), hypernets

def find_abas(name) :
    abas = []
    for i in range(len(name)-2) :    
        if name[i] == name[i+2] and name[i] != name[i+1] :
            abas.append(name[i:i+3])
    return abas

bab = lambda s : s[1] + s[0] + s[1]
def is_ssl(ip) :
    supernets, hypernets = ip_parts(ip)
    abas = [ aba for sup in supernets for aba in find_abas(sup)  ]
    
    for hypernet in hypernets :   
        for aba in abas :
            if bab(aba) in hypernet : return 1
    
    return 0


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result = p2_result = 0
    for ip in aoc_input.splitlines() :
        p1_result += is_tls(ip)
        p2_result += is_ssl(ip)

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
