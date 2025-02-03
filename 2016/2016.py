#!python3
#############
'''Wrapper for 2016 AoC Python puzzle solver'''
import sys
import importlib
from os import access, R_OK
from os.path import isfile
import aoc

YEAR = '2016'

for arg in sys.argv[1:] :

    if arg == 'stat' :
        aoc.print_statistics(YEAR)
        sys.exit(0)

    if arg == 'all' :
        puzzles = [ f'{day:02d}' for day in range (1,26) ]
    else :
        puzzles = [ arg ]

    for day in puzzles :
        fname = YEAR + '_' + day
        if isfile(fname+'.py') and access(fname+'.py', R_OK) :
            puzzle = importlib.import_module(fname)
            aoc.init(puzzle)
            aoc.run_tests(puzzle)
            aoc.run_puzzle(puzzle)
