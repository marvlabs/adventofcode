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
    'name'          :   "Medicine for Rudolph - One heck of a complex Moli",
    'difficulty'    :   'D3',
    'learned'       :   'Ufff, not everything is computed. Semantics helps',
    't_used'        :   '300',
    'result_p1'     :   576,
    'result_p2'     :   207
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
    'p2' : None,#6,
},

{
    'name'  : 'Constructed for P2', # e->OMg = OMg (2), O->HP = HPMg (3), P->SiRnFAr = HSiRnFArMg (6)
    'input' : '''
e => OMg
O => HP
P => SiRnFAr

HSiRnFArMg
''',
    'p1' : None,
    'p2' : 3,
},


]
#################

# P1: the easy part: split the molecule into single atoms, then replace each one of them with all possible replacements.
# Creates a set of results
def nr_of_fusions(molecule, replacements):
    mols = set()
    atoms = re.findall(r'[A-Z][a-z]?', molecule)
    for i, atom in enumerate(atoms):
        if atom in replacements :
            mols.update( ''.join(atoms[:i]) + rep + ''.join(atoms[i+1:]) for rep in replacements[atom]  )
    return len(mols)


# P2: Brute force forward -> No chance
# Brute force reverse: Not found a solution yet, tried recursive and an A* gready search
# ...
# Ok, after some exernal pointers -> looking closer at the input. We find:
def unproducing_atoms(molecule, replacements) :
    atoms = re.findall(r'[A-Z][a-z]?', molecule)
    unproducing = { atom for atom in atoms if atom not in replacements }
    print (f'UNPRODUCING ATOMS: {unproducing}')
# -> Ar Rn Y
#
# There are atoms which cannot be replaced (no replacement rules).
# We see rules generating them, all of which look like
#     xRnx(Yx)*Ar, i.e. H => CRnFYMgAr or H => CRnAlAr   ---> [A-Z][a-z]?Rn.*?(Y.*?)*?Ar
#   We can therefore split the Molecule into simpler parts? 
#   Thinking of these three as
#     Rn == (
#     Ar == )
#      Y == ,
#   ORnPBPMgArCaCaCaSiThCaCaSiThCaCaPBSiRnFArRnFArCaCaSiThCaCaSiThCaCaCaCaCaCaSiRnFYFArSiRnMgArCaSiRnPTiTiBFYPBFArSiRnCaSiRnTiRnFArSiAlArPTiBPTiRnCaSiAlArCaPTiTiBPMgYFArPTiRnFArSiRnCaCaFArRnCaFArCaSiRnSiRnMgArFYCaSiRnMgArCaCaSiThPRnFArPBCaSiRnMgArCaCaSiThCaSiRnTiMgArFArSiThSiThCaCaSiRnMgArCaCaSiRnFArTiBPTiRnCaSiAlArCaPTiRnFArPBPBCaCaSiThCaPBSiThPRnFArSiThCaSiThCaSiThCaPTiBSiRnFYFArCaCaPRnFArPBCaCaPBSiRnTiRnFArCaPRnFArSiRnCaCaCaSiThCaRnCaFArYCaSiRnFArBCaCaCaSiThFArPBFArCaSiRnFArRnCaCaCaFArSiRnFArTiRnPMgArF
#   O (PBPMg) CaCaCaSiThCaCaSiThCaCaPBSi (F)  (F) CaCaSiThCaCaSiThCaCaCaCaCaCaSi (F,F) Si (Mg) CaSi (PTiTiBF,PBF) Si (CaSi (Ti (F) SiAl) PTiBPTi (CaSiAl) CaPTiTiBPMg,F) PTi (F) Si (CaCaF)  (CaF) CaSi (Si (Mg) F,CaSi (Mg) CaCaSiThP (F) PBCaSi (Mg) CaCaSiThCaSi (TiMg) F) SiThSiThCaCaSi (Mg) CaCaSi (F) TiBPTi (CaSiAl) CaPTi (F) PBPBCaCaSiThCaPBSiThP (F) SiThCaSiThCaSiThCaPTiBSi (F,F) CaCaP (F) PBCaCaPBSi (Ti (F) CaP (F) Si (CaCaCaSiThCa (CaF) ,CaSi (F) BCaCaCaSiThF) PBF) CaSi (F)  (CaCaCaF) Si (F) Ti (PMg) F
#
#  All other rules (!) are of the form : x -> yz , so every yz needs one reverse replacement to go back to x

# Conclusion: 
# - Every xRnyAr backwards replacement reduces the length of the molecule by three in one step, 
#   giving factor two for each Rn-Ar combo, or one for each (without the (Yx)* part)
# - Every Yx included in the above reduces further by 2*Y (in the same step)
# - The rest needs to be reduced by XX->X , therefore needing len - 1 steps
# ==> steps until one e left: nr_of_atoms - nr_of_Rn_and_Ar - 2*nr_of_Y - 1

def nr_of_substitutions(molecule) :
    return nr_of_atoms(molecule) - 2*molecule.count('Rn') - 2*molecule.count('Y') - 1


def nr_of_atoms(molecule) :
    return len(re.findall(r'[A-Z]', molecule))
assert nr_of_atoms('CRnFYFArRnPBP') == 10


def solve(aoc_input, part1=True, part2=True, attr=None) :
    '''called from wrapper or main, if run directly'''

    replacements = {}
    strings = aoc_input.splitlines()
    molecule = strings[-1]
    for string in strings[0:-2] :
        if string == '' : continue
        mol, rep = re.match(r'(.*) => (.*)', string).groups()
        replacements.setdefault(mol, []).append(rep)

    p1_result = nr_of_fusions(molecule, replacements)

    #unproducing_atoms(molecule, replacements))
    p2_result = nr_of_substitutions(molecule)
    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
