#!python3
'''AoC 2024 Day 05'''
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '05',
    'url'           :   'https://adventofcode.com/2024/day/05',
    'name'          :   "Print Queue: order those jobs",
    'difficulty'    :   'D2',
    'learned'       :   'Precision thinking in loops',
    't_used'        :   '30',
    'result_p1'     :   6260,
    'result_p2'     :   5346,
}
#############
TESTS = [
 {
        'name'  : 'PQueue-1',
        'input' : '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47''',
        'p1' : 143,
        'p2' : 123,
    },
]
#################

Rules = { i: [] for i in range(100) }

def job_good(job) :
    for i in range(1, len(job)):
        for j in range(i) :
            if job[j] in Rules[job[i]] :
                return False
    return True


# 75,97,47,61,53 becomes 97,75,47,61,53.
# 61,13,29 becomes 61,29,13.
# 97,13,75,29,47 becomes 97,75,47,29,13.
def fix_job(job) :
    last_order = []
    while len(job) > 0 :
        for page in job :
            page_last = True
            for p in job :
                if p in Rules[page] :
                    page_last = False; 
                    break
            if page_last :
                last_order.append(page)
                job.remove(page)
    return list(reversed(last_order))


def solve(aoc_input, part1=True, part2=True, attr=None) :
    p1_result, p2_result = 0, 0

    get_rules = True
    for string in aoc_input.splitlines()  :
        if string == '' : 
            get_rules = False
            continue
        if get_rules :
            p1, p2 = string.split('|')
            Rules[int(p1)].append(int(p2))
        else :
            job = list(map(int, string.split(',')))
            if job_good(job) :
                p1_result += job[len(job) // 2]
            else :
                fixed = fix_job(job)
                p2_result += fixed[len(fixed) // 2]

    return p1_result, p2_result

#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
