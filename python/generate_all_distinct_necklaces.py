# Takes an integer and returns all distinct 2n necklaces of that length. Strings are considered identical necklaces if:
# * they are a cyclic permutation of one another:                       e.g. 1010   == 0101
# * they are a mirroring of one another:                                e.g. 101100 == 001101
# * they are a cyclic permutation of a mirroring of one another:        e.g. 101100 == 011010


from itertools import combinations, chain
import numpy as np
import sys


def binary_words(zeros, ones):
    n = zeros + ones
    for c in combinations(range(n), ones):
        word = np.zeros(n, dtype=int)
        word[list(c)] = 1
        yield tuple(word)


def cyclic_permute(word):
    for i in range(len(word)):
        yield word[i:] + word[:i]


def dihedral_permute(word):
    return chain(cyclic_permute(word), cyclic_permute(word[::-1]))


def is_reduced(word):
    return all(word <= w for w in dihedral_permute(word))


def balanced_necklaces(n):
    return list(filter(is_reduced, binary_words(n, n)))


def strings_balanced_necklaces(n):
    ret = [''.join(map(str,necklace)) for necklace in balanced_necklaces(n)]
    return ret


def main():
    [print(string) for string in strings_balanced_necklaces(int(sys.argv[1]))]


if __name__ == "__main__":
   # not called via import
    main()
