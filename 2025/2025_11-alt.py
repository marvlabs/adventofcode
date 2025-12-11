#!python3
'''AoC 2025 Day 11'''
#############
CONFIG = {
    'year'          :   '2025',
    'day'           :   '11',
    'url'           :   'https://adventofcode.com/2025/day/11',
    'name'          :   "Day 11: Reactor - pass fft dac on the way out",
    'difficulty'    :   'D2',
    'learned'       :   'recursing in AoC always needs a cache',
    't_used'        :   '10',
    'result_p1'     :   543,
    'result_p2'     :   479511112939968,
}
#############
TESTS = [
 {
        'name'  : 'you-out',
        'input' : '''
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
''',
        'p1' : 5,
        'p2' : None,
    },
 {
        'name'  : 'svr-fft-dac-out',
        'input' : '''
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
''',
        'p1' : None,
        'p2' : 2,
    },]
#################

# Alternative version: Only one way_out function without carrying the dac and fft bools, but called for the two cases of the possible paths
# Cleaner? A bit less efficient. But nicer to look at?
# ...and with my own cache, just for the heck of it
def way_out(devices, seen, start, target) :
    if (start, target) in seen : return seen[(start, target)]
    if start == target : return 1
    if start == 'out'  : return 0
    ways = sum( way_out(devices, seen, d, target) for d in devices[start] )
    seen[(start, target)] = ways
    return ways

def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0

    devices = { d_in[:-1] : d_out for d_in, *d_out in [ line.split() for line in aoc_input.splitlines()  if line != '' ] }
    seen = {}
    if part1 : p1_result = way_out(devices, seen, 'you', 'out')
    if part2 : p2_result = (
        way_out(devices, seen, 'svr', 'fft') *  way_out(devices, seen, 'fft', 'dac') * way_out(devices, seen, 'dac', 'out') + 
        way_out(devices, seen, 'svr', 'dac') *  way_out(devices, seen, 'dac', 'fft') * way_out(devices, seen, 'fft', 'out') )

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
