# idea:
# if you can prove that some algorithm:
# 1. never stops, that is, always changes some part of the string when its partitioned a certain way, and
# 2. always reaches all strings,
# then you can prove that the algo always will reach a valid config eventually

import sys
import random
from itertools import permutations

window_size = 6 # for now t = w
num_of_strings_to_test = 50000

class algorithm:
    def __init__(self):
        self.rules = {}

    def add_rule(self, int, str):
        self.rules[int] = str


def all_permutations(string):
    permutation_list = []
    permsList = permutations(string)

    for perm in permsList:
        permutation_list.append(''.join(perm))

    return permutation_list

# partitions a string, allows shifting
def partition_string(str, window_size: int, shift: int):
    partitions = []
    for i in range(0, len(str), window_size):
        partitions.append(str[i+shift:i+window_size+shift])

    # add the beginning of the string to the last partition
    partitions[-1] += (str[:shift])
    return partitions


def run_algorithm_on_a_single_full_shift(str, algorithm, window_size: int):
    shift = 0
    for i in range(0, window_size):
        shift = (shift + 1) % window_size
        partitions = partition_string(str, window_size, shift)
        for j in range(0, len(partitions)):
            count = partitions[j].count('0')
            if count in algorithm.rules:
                partitions[j] = algorithm.rules[count]
                string = "".join(partitions)
    return("".join(partitions))


# shuffles a string
def shuffle(string):
    return ''.join(random.sample(string,len(string)))


def main():
    if len(sys.argv) < 7:
        print('Error: invalid algorithm given.')
        print(sys.argv)
        sys.exit(0)

    else:
        string = "0"* int(window_size*5) + "1"* int(window_size*5)

        alg = algorithm()
        alg.add_rule(int(sys.argv[1]), sys.argv[2])
        alg.add_rule(int(sys.argv[3]), sys.argv[4])
        alg.add_rule(int(sys.argv[5]), sys.argv[6])

        print('testing algorithm' + str(alg.rules))
        for i in range(0, num_of_strings_to_test):
            print('Testing on string ' + str(i), end='\r')
            string = shuffle(string)
            if run_algorithm_on_a_single_full_shift(string, alg, window_size) == string:
                #print('\nFailed on string ' + string)
                sys.exit(0)
        print('algorithm ' + str(alg.rules) + 'succeeded!')

main()
