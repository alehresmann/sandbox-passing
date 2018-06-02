# Takes a cyclical string as input and returns all distinct permutations of that string. Strings are considered identical if:
# * they are a cyclic permutation of one another:                       e.g. 1010   == 0101
# * they are a mirroring of one another:                                e.g. 101100 == 001101
# * they are a cyclic permutation of a mirroring of one another:        e.g. 101100 == 011010

# Anne-Laure Ehresmann

import sys
from itertools import permutations

def all_permutations(string):
    permutation_list = []
    permsList = permutations(string)

    for perm in permsList:
        permutation_list.append(''.join(perm))

    return permutation_list


def cyclic_shifts(string):
    cyclic_shifts_list = []
    if len(string) == 1:
        return [string]
    else:
        for char in string:
            string = ''.join([string[1:],string[0]])
            cyclic_shifts_list.append(string)
    return cyclic_shifts_list


def main():
    if len(sys.argv) < 2:
        print('Error: not input string given.')
        sys.exit(0)

    else:
        inpt = str(sys.argv[1])
        perms = all_permutations(inpt)

        distinct_permutations = []

        for current in perms:
            if len(distinct_permutations) == 0:
                distinct_permutations.append(current)
            else:
                is_distinct = True
                for distinct in distinct_permutations:
                    shifts = cyclic_shifts(distinct)
                    for s in shifts:
                        if current == s:
                            #print(current + ' same as ' + s)
                            is_distinct = False
                        if current == s[::-1]:
                            #print(current + ' same as ' + s[::-1])
                            is_distinct = False # if same as inversed string

                if is_distinct: distinct_permutations.append(current)

        for distinct in distinct_permutations:
            print(distinct)

main()
