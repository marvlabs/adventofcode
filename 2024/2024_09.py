#!python3
'''AoC 2024 Day 09'''
# from pprint import pprint as pp
import copy
#############
CONFIG = {
    'year'          :   '2024',
    'day'           :   '09',
    'url'           :   'https://adventofcode.com/2024/day/09',
    'name'          :   "Disk Fragmenter: move those blocks",
    'difficulty'    :   'D2',
    'learned'       :   'Deepcopy. And: It\'s easy to make a lot of mistakes...',
    't_used'        :   '60',
    'result_p1'     :   6356833654075,
    'result_p2'     :   6389911791746,
}
#############
TESTS = [
 {
        'name'  : 'Disk-1',
        'input' : '''2333133121414131402''',
        'p1' : 1928,
        'p2' : 2858,
    },
]
#################

def parse_diskmap(aoc_input):
    files = {}
    freemap = []

    current_block=0
    for i, c in enumerate(aoc_input) :
        if c == '\n' : break
        file_length = int(c)
        if i % 2 == 0 :
            files[i // 2] = [ current_block+j for j in range(file_length) ]
        else :
            freemap += [ current_block+j for j in range(file_length) ]
        current_block += file_length
    print("last block", current_block)
    return files,freemap


def checksum(files) :
    return sum(block*file_id for file_id in files.keys() for block in files[file_id] )


def defragment_blocks(freemap, files) :
    defragmented = False
    freeblock_id = 0
    for id in sorted(files.keys(), reverse=True) :
        #print (f'defragmenting {id}')
        if defragmented: break

        file_length = len(files[id])
        for fileblock_id in range(file_length-1, -1, -1) :
            if defragmented: break
            
            freeblock = freemap[freeblock_id]
            fileblock = files[id][fileblock_id]
            if fileblock > freeblock :
                files[id][fileblock_id] = freeblock
                freemap[freeblock_id] = fileblock
                freeblock_id += 1
                #print (f"move {fileblock} to {freeblock}")
            else :
                defragmented = True
    return files


def find_contiguous(freemap, at_least) :
    if (at_least == 1) : return 0 # first entry in freemap is good enough for a one-block file

    contiguous = 1
    id = 0
    for i in range(1, len(freemap)) :
        if freemap[i] - freemap[i-1] == 1 :
            contiguous += 1
            if contiguous >= at_least :
                return id
        else :
            contiguous = 1
            id = i

    return -1


# Don't swap blocks into the freemap when moving file - delete the used entries and append the free ones to the end.
# This saves a lot of time because we don't need to sort the freemap every time.
def defragment_files(freemap, files) :
    for id in sorted(files.keys(), reverse=True) :
        #print (f'trying to defragment file {id} with size {len(files[id])}')
        file_length = len(files[id])
        freeblock_id = find_contiguous(freemap, file_length)
        if freeblock_id == -1 : continue
        if freemap[freeblock_id] > files[id][0] :
            if file_length == 1 : break # No longer any lower space available for 1-block files, we can stop checking
            continue

        # Move file to free space found above
        freemap.extend(files[id])
        files[id] = freemap[freeblock_id:freeblock_id+file_length]
        del freemap[freeblock_id:freeblock_id+file_length]

    return files



def solve(aoc_input, part1=True, part2=True, attr=None) :
    files, freemap = parse_diskmap(aoc_input)

    # store copy for part 2
    freemap_p2 = freemap.copy()
    files_p2 = copy.deepcopy(files)

    p1_result = checksum(defragment_blocks(freemap, files))
    p2_result = checksum(defragment_files(freemap_p2, files_p2))

    return p1_result, p2_result


#############
if __name__ == '__main__' :
    import sys
    import aoc
    puzzle = sys.modules[__name__]

    aoc.init(puzzle)
    aoc.run_tests(puzzle)
    aoc.run_puzzle(puzzle)
