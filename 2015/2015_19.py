#!python3
'''AoC 2015 Day 19'''
# from pprint import pprint as pp
import re
from collections import Counter
from random import shuffle
from queue import PriorityQueue

#############
CONFIG = {
    'year'          :   '2015',
    'day'           :   '19',
    'url'           :   'https://adventofcode.com/2015/day/19',
    'name'          :   "Medicine for Rudolph",
    'difficulty'    :   'D',
    'learned'       :   '',
    't_used'        :   '0',
    'result_p1'     :   576, # not 670
    'result_p2'     :   0, #207
}
#############
TESTS = [
    {
        'name'  : 'Simple HOH',
        'input' : '''
e => H
e => O
H => HO
H => OH
O => HH

HOH
''',
        'p1' : 4,
        'p2' : None,#3,
    },
    {
        'name'  : 'Simple HOHOHO',
        'input' : '''
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
''',
        'p1' : 7,
        'p2' : None,#5,
    },
]
#################
def nr_of_fusions(molecule, repl):
    #mols = Counter()
    mols = set()
    atoms = re.findall(r'[A-Z][a-z]?', molecule)
    for i, atom in enumerate(atoms):
        if atom in repl :
            mols.update( ''.join(atoms[:i]) + rep + ''.join(atoms[i+1:]) for rep in repl[atom]  )
    #print (sorted(mols))
    return len(mols)

def nr_of_atoms(molecule) :
    return len(re.findall(r'[A-Z]', molecule))
assert nr_of_atoms('CRnFYFArRnPBP') == 10

def nr_of_fissions(molecule, repl):
    reverse = { target : source for source in repl.keys() for target in repl[source]  }
    fissions = sorted(reverse.keys(), key=lambda k: len(reverse[k]), reverse=True)
    #shuffle(fissions)

    cost_current = 0
    seen = [ (molecule, cost_current) ]

    checks = 0
    while seen:
        checks += 1
        #mol_current = sorted(seen.keys(), key=lambda m : seen[m]['cost'] + seen[m]['estimate'], reverse=True)[0]
        mol_current, cost_current = seen.pop()

        if checks % 1 == 0 :
            print('checking', checks, mol_current, cost_current, len(seen))

        new_mols = []
        for fission in reverse.keys():#fissions:
            for match in re.finditer(fission, mol_current):
                mol_new = mol_current[:match.start()] + reverse[fission] + mol_current[match.end():]

                #if re.match(r'^e+$', new_molecule):
                if mol_new == 'e':
                    print ('  found e', cost_current)
                    return cost_current+1
                
                if reverse[fission] == 'e':
                    # don't want any molecules with an e, unless it's the last one
                    continue

                #print ('  adding', cost_current, mol_new)
                new_mols.append((mol_new, cost_current+1))
                #seen[mol_new] = { 'cost': cost_current, 'estimate':len(mol_new)//8}
        seen.extend(sorted(sorted(new_mols, reverse=True), key=len))
        


    raise SystemExit("FATAL: no solution found")



def nr_of_fissions_a_star(molecule, repl):
    reverse = { target : source for source in repl.keys() for target in repl[source]  }
    fissions = sorted(reverse.keys(), key=lambda k: len(reverse[k]), reverse=True)
    #shuffle(fissions)

    checked = {}
    seen = { molecule:{ 'cost': 0, 'estimate':nr_of_atoms(molecule) // 3 } }
    cost_current = 0

    checks = 0
    while seen:
        checks += 1
        mol_current = sorted(seen.keys(), key=lambda m : seen[m]['cost'] + seen[m]['estimate'], reverse=True)[0]
        checked[mol_current] = seen[mol_current]
        del seen[mol_current]
        cost_current = checked[mol_current]['cost'] + 1

        if checks % 1 == 0 :
            #print('checking', checks, cost_current)
            print('Checking', checks, cost_current, mol_current, checked[mol_current])

        for fission in fissions:
            for match in list(reversed(list(re.finditer(fission, mol_current)))):
                mol_new = mol_current[:match.start()] + reverse[fission] + mol_current[match.end():]

                #if re.match(r'^e+$', new_molecule):
                if mol_new == 'e':
                    print ('  found e', cost_current)
                    return cost_current
                
                if reverse[fission] == 'e':
                    # don't want any molecules with an e, unless it's the last one
                    continue

                if mol_new in seen:
                    if seen[mol_new]['cost'] <= cost_current:
                        pass#print('  already seen cheaper', mol_new)
                    else:
                        print('  found cheaper', cost_current, mol_new)
                        seen[mol_new]['cost'] = cost_current
                    continue

                if mol_new in checked:
                    if checked[mol_new]['cost'] <= cost_current:
                        pass#print('  aldready checked', mol_new)
                    else:
                        print('  already checked, but found cheaper', cost_current, mol_new)
                        checked[mol_new]['cost'] = cost_current
                        seen[mol_new] = checked[mol_new]
                    continue

                #print ('  adding', cost_current, mol_new)
                seen[mol_new] = { 'cost': cost_current, 'estimate':nr_of_atoms(mol_new) // 5}
                #seen[mol_new] = { 'cost': cost_current, 'estimate':len(mol_new)//8}

    raise SystemExit("FATAL: no solution found")



def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''

    repl = {}
    strings = aoc_input.splitlines()
    molecule = strings[-1]
    for string in strings[0:-2] :
        if string == '' : continue
        mol, rep = re.match(r'(.*) => (.*)', string).groups()
        repl.setdefault(mol, []).append(rep)

    #print(molecule)
    #print(repl)
    p1_result = nr_of_fusions(molecule, repl)
    p2_result = nr_of_fissions(molecule, repl)
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)


# def nr_of_fissions(molecule, repl):
#     reverse = { target : source for source in repl.keys() for target in repl[source]  }
#     fissions = list(sorted(reverse.keys(), key = lambda k : len(reverse[k])))

#     new_molecule = molecule
#     replacements = 0

#     while True:
#         shuffle(fissions)
#         new_molecule = molecule
#         replacements = 0

#         for fission in fissions:
#             while fission in new_molecule:
#                 new_molecule = new_molecule.replace(fission, reverse[fission], 1)
#                 replacements += 1
#                 #if re.match(r'^e+$', new_molecule):
#                 print (new_molecule)
#                 if new_molecule == 'e':
#                     return replacements

#         #print(replacements, new_molecule)
