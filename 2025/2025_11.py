#!python3
'''AoC 2025 Day 11'''
import functools
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
Devices = {}

def way_out(device) :
    if device == 'out' : return 1
    return sum( way_out(d) for d in Devices[device] )


@functools.cache
def way_out2(device, has_fft, has_dac) :
    if device == 'out' : 
        if has_fft and has_dac : return 1
        return 0
    if device == 'fft' : has_fft = True
    if device == 'dac' : has_dac = True
    return sum( way_out2(d, has_fft, has_dac) for d in Devices[device] )    


def solve(aoc_input, part1=True, part2=True, attr=None) :
    global Devices
    Devices = {}
    way_out2.cache_clear()
    p1_result, p2_result = 0, 0

    Devices = { d_in[:-1] : d_out for d_in, *d_out in [ line.split() for line in aoc_input.splitlines()  if line != '' ] }
    if part1 : p1_result = way_out('you')
    if part2 : p2_result = way_out2('svr', False, False)
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
