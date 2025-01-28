''' AdventOfCode Scaffolding 
Uses: puzzle solving modules
Needs: puzzle.CONFIG dict'''
###
import json
import time
import os

import urllib.request
# Either use certify (pip install certify, then use the explicit CA file context in the request (context=ssl.create_default_context(cafile=certifi.where())))
# or run: sudo "/Applications/Python 3.12/Install Certificates.command" to get the certificates
# Since python does no longer use the root CAs from MacOS as default
import certifi
import ssl
#import requests
###
STATISTICS = {}

def init(puzzle) :
    '''Init will be used for stats etc later
    arg: the puzzle solving module to be used, eg. 2015_01
    prints: puzzle title'''
    print ('AdventOfCode', puzzle.CONFIG['year'], '- Day', puzzle.CONFIG['day'], ':', puzzle.CONFIG['name'])
    _load_statistics(puzzle.CONFIG['year'])
    input_filename = f"input/{puzzle.CONFIG['day']}.txt"
    if not os.path.isfile(input_filename) :
        _download_input(input_filename, puzzle.CONFIG['year'], puzzle.CONFIG['day'])
    puzzle.CONFIG['INPUTFILE'] = input_filename


def run_tests(puzzle) :
    '''Iterates through the test cases, runs them and exits if a test fails
    arg: the puzzle solving module to be used, eg. 2015_01
    needs: puzzle.TESTS dict
    prints: test results'''
    print ('Tests:')
    start_test = time.time()

    for test in puzzle.TESTS:
        print ('   ', test['name'], ':', end='')
        p1, p2 = puzzle.solve(test['input'], part1=(test['p1'] != None), part2=(test['p2'] != None), attr=test['testattr'] if 'testattr' in test else None)

        for part in ('p1', 'p2') :
            if test[part] != None:
                result = p1 if part == 'p1' else p2
                if result == test[part] :
                    print ('  ', part, 'ok', end='')
                else:
                    print ('  ', part, 'FAIL: expected', test[part], 'but got', result)
                    exit(1)
        print()

    time_used = time.time() - start_test
    puzzle.CONFIG['testtime'] = time_used


def run_puzzle(puzzle) :
    '''Load the puzzle input and call the solving function
    arg: the puzzle solving module to be used, eg. 2015_01
    prints: the results p1 and p2'''
    print ('Puzzle:')
    aoc_input = _get_input(puzzle.CONFIG['INPUTFILE'])
    start_solve = time.time()
    p1, p2 = puzzle.solve(aoc_input)
    time_used = time.time() - start_solve
    puzzle.CONFIG['runtime'] = time_used
    print ('   Part 1: ' + str(p1))
    print ('   Part 2: ' + str(p2))
    _store_statistics(puzzle.CONFIG)


def _load_statistics(year) :
    '''Get the statistics from file, so that we can add the current run'''
    global STATISTICS
    try:
        fp=open(year + '_stat.json','r')
        STATISTICS = json.load(fp)
        fp.close()
    except Exception as err:
        STATISTICS = {}


def _store_statistics(config) :
    '''Persist the statistics to file. Add the currently run puzzle config to it'''
    STATISTICS[config['day']] = config
    fp = open(config['year'] + '_stat.json','w')
    json.dump(STATISTICS, fp)
    fp.close()


def _get_input(filename) :
    '''Read puzzle input in one go
    arguments: input file name
    returns: string with puzzle input, possibly multiline'''
    aocInputFile = open(filename, mode='r')
    aocInput = aocInputFile.read()
    aocInputFile.close()
    return aocInput


def _get_aoc_session() :
    if 'AOC_SESSION' in os.environ :
          return os.environ['AOC_SESSION']

    aoc_session_file = '../aoc-session-key.secret'
    if os.path.isfile(aoc_session_file) :
          print ('reading session file')
          return _get_input(aoc_session_file)
    raise SystemExit("FATAL: AOC_SESSION not found")


def _download_input(fname, year, day) :
    '''Get the personalize input from AoC. Use session cookie from file or env'''
    print (f'AOC input download: {fname} {year}/{day}')
    session = _get_aoc_session()

    url = f'https://adventofcode.com/{year}/day/{day}/input'
    #url = f'http://localhost:1234/{year}/day/{day}/input'
    req = urllib.request.Request(url, headers={'Accept': '*/*', 'Accept-Encoding': '*', 'Cookie': f'session={session}'})
    # handler = urllib.request.HTTPSHandler(debuglevel=10)
    # opener = urllib.request.build_opener(handler)
    # input = opener.open(req).read().decode()
    input = urllib.request.urlopen(req,  context=ssl.create_default_context(cafile=certifi.where())).read().decode()

    # input = requests.get(url, cookies={'session': session}).content.decode()
    # print (input)

    f = open(fname, 'w')
    f.write(input)
    f.close()


def print_statistics(year) :
    '''Output the gathered statistics of all runs'''
    _load_statistics(year)

    runtime = worktime = 0
    print ("Advent of Code 2023                               Tests [run time]  Puzzle [Difficulty, work time, run time]      lessons learned")
    print ("---------------------------------------------------------------------------------------------------------------------------------------")
    for day, stat in sorted(STATISTICS.items()) :
        runtime += int(stat['runtime'])
        worktime += int(stat['t_used'])
        t = int(stat['t_used'])
        print(f"{year}-{stat['day']} {stat['name']:55s} {stat['testtime']:7.3f}s   {stat['difficulty']}  {t//60:d}:{t%60:02d}  {stat['runtime']:7.3f}s   {stat['learned']}")
    print ("---------------------------------------------------------------------------------------------------------------------------------------")
    print (f"Advent of Code 2023 Total:   work {worktime//60}h{worktime%60}m,   runtime {runtime} seconds")