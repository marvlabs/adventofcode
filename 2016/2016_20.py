#!python3
'''AoC 2016 Day 20'''
#############
CONFIG = {
    'year'          :   '2016',
    'day'           :   '20',
    'url'           :   'https://adventofcode.com/2016/day/20',
    'name'          :   "Firewall Rules - lots of ranges",
    'difficulty'    :   'D2',
    'learned'       :   'Ranges are ... bleh',
    't_used'        :   '30',
    'result_p1'     :   32259706,
    'result_p2'     :   113,
}
#############
TESTS = [
{
    'name'  : 'sometest',
    'input' : '''5-8
0-2
4-7''',
    'p1' : 3,
    'p2' : 2,
    'testattr': 9,
},
]
#################
# Oh my. The rules are so broad that consolidating and ordering them was REALLY not worth it.
# Bleh. 
# BF with forwarding to the end of a range is very efficient when only a couple hundred IPs pass in the end.
# Mhmmm, maybe this could be used efficiently as well with sparse rules? Do the above, and once in 'free' space, forward to the next low bound and continue there.
# My way was overkill...


# The rule sorter way:
# This takes all rules and compresses the ones that overlap or are adjacent.
# Afterwards, if ordered, we can take the first space and sum up the spaces
def consolidate_rules(rules) :
    new_rules = rules.copy()
    consolidated = []

    while len(new_rules) :
        vetted_rules = []
        r_new = new_rules.pop()
        
        # Test the next new rule against all already seen
        while len(consolidated) :
            r = consolidated.pop()

            if r_new[0] >= r[0] and r_new[1] <= r[1] :
                # new rule contained in existing rule
                vetted_rules.append(r)
                r_new = None
                break
        
            if r[0] >= r_new[0] and r[1] <= r_new[1] :
                # existing rule contained in new rule, r no longer necessary
                continue

            if r_new[0] < r[0] and r_new[1] >= r[0]-1 :
                # New rule extends lower bounds of existing -> scratch both rules and add combined to the new rules, and re-start checking
                new_rules.append((r_new[0], r[1]))
                r_new = None
                break

            if r_new[0] <= r[1]+1 and r_new[1] > r[1] :
                # New rule extends upper bounds of existing -> scratch both rules and add combined to the new rules, and re-start checking
                new_rules.append((r[0], r_new[1]))
                r_new = None
                break
            
            vetted_rules.append(r) # the rule still holds

        if r_new :
            vetted_rules.append(r_new) # the new rule is ok for now

        vetted_rules.extend(consolidated) # re-add the ones that we didn't check in this pass
        consolidated = vetted_rules

    return consolidated


# Brute force: much better after finding that the rules exclude almost everything...
# Could be further optimized fast-forwarding through free-space if large allowed ranges occured
def just_check_em(rules, max_ip) :
    i = 0
    lowest = None
    count = 0

    while i <= max_ip:
        for lower, upper in rules:
            if lower <= i <= upper:
                i = upper
                break
        else:
            if lowest is None : lowest = i
            count += 1
        i += 1    

    return lowest, count


def solve(aoc_input, part1=True, part2=True, attr=None) :
    max_ip = 4294967295 if not attr else attr

    rules = [ tuple(map(int, line.split('-'))) for line in aoc_input.splitlines() ]
    p1_result, p2_result = just_check_em(rules, max_ip)

    #rules_sorted = sorted(consolidate_rules(rules), key=lambda x: x[0])
    # p1_result = rules_sorted[0][1]+1 if rules_sorted[0][0] == 0 else 0
    # for i in range(len(rules_sorted)-1) :
    #     p2_result += rules_sorted[i+1][0] - rules_sorted[i][1] - 1
    # if rules_sorted[-1][1] != max_ip: p2_result += max_ip - rules_sorted[-1][1]

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
