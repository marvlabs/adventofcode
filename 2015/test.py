#! python3
import re
from itertools import product

########################
# Combine generators
def combine_4_items_loop(x) :
    for a in range(0,x+1) :
        for b in range(0,x+1-a) :
            for c in range(0, x+1-a-b) :
                d = x - a - b - c
                yield(a,b,c,d,)


def combine_4_items_comprehension(x) :
    return ( (a,b,c,x-a-b-c) for a in range(0,x+1) for b in range(0,x+1-a) for c in range(0, x+1-a-b) ) 
def combine_3_items_comprehension(x) :
    return ( (a,b,x-a-b) for a in range(0,x+1) for b in range(0,x+1-a) ) 
def combine_2_items_comprehension(x) :
    return ( (a,x-a) for a in range(0,x+1) ) 


# def combine_items_to_x(items, x) :
#     '''Generator - yield all tuple combinations with items for x slots'''
#     for i in range(x+1) :
#         if items == 1 :
#             yield (i,)
#         elif items == 2 :
#             yield (i,x-i,)
#         else :
#             for combine in combine_items_to_x(items-1, x-i) :
#                 yield (i,) + combine
#     return


def combine_items_to_x(items, x) :
    '''Generator - yield all tuple combinations with items for x slots
    items: how many items to assign
    x: how many slots. > 0
    returns: Generator for all possible tuples, i.e. (2,3) -> (0, 3) (1, 2) (2, 1) (3, 0)'''
    if items == 1 :
        yield (x,)
        return
    for i in range(x+1) :
        for sub in combine_items_to_x(items-1, x-i) :
            yield (i,) + sub
    return

def combine_items_to_x_comprehend(items, x) :
    '''Generator - yield all tuple combinations with items for x slots
    items: how many items to assign
    x: how many slots. > 0
    returns: Generator for all possible tuples, i.e. (2,3) -> (0, 3) (1, 2) (2, 1) (3, 0)'''
    if items == 1 :
        yield (x,)
        return
    for i, sub in ((i,sub) for i in range(x+1) for sub in combine_items_to_x_comprehend(items-1, x-i)) :
        yield (i,) + sub
    return

def test_generator() :
    count = 0
    #for t in combine_items_to_x1(4,10) :
    #for t in combine_4_items_comprehension(10) :
    #for t in combine_4_items_loop(10) :

    #for t in combine_2_items_comprehension(10) :
    #for t in combine_4_items_comprehension(100) :
    for t in combine_items_to_x(4,100) :
    #for t in combine_items_to_x_comprehend(4,100) :
        #print(t)
        count += 1
    print(count)


#########################
# array, slice
def test_nums() :
    nums = [ x for x in range(2, 9)]
    print ('nums:', nums)
    print ('3-5', nums[3:5])

    nums[3:5] = map(lambda x : x+10, nums[3:5])
    print ('nums:', nums)

    r = slice(3,5)
    nums[r] = map(lambda x : x+10, nums[r])
    print ('nums:', nums)

########################
# regex
def test_regex() :
    l = ['a'] + [ c for c in ['b', 'c'] ]
    print (l)
    print (sum(map(int,(re.findall(r'-?\d+', 'ab1cd23ef-456gh')))))

########################
def test_comprehension() :
    l = [x for x in [a for a in range(10)] if x%2==0 ]
    print(l)

    for x in range(5) :
        for i in range ( 5 - x ) :
            print ((x,i,))

    for x, i in ((x, i,) for x in range(5) for i in range (5-x)) :
        print ((x,i,))

def test_product() :
    l = [2,3,3,4]
    perms = product([0,1], repeat=len(l))
    prods = ( [x*y for x,y in zip(l, perm)] for perm in perms  )
    sums = [ sum (prod) for prod in prods ]
    count = sum(s == 9 for s in sums)
    print(list(sums), count)

    perms = [product([0,1], repeat=len(l))] # [] NOT the same as list(...)
    print (perms)


########################
if __name__ == '__main__' :
    test_product()
    #test_comprehension()
    #test_generator()
    #test_regex()
    #test_nums()
