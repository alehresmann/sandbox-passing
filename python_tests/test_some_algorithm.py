# tests a particular algorithm on a bunch of strings.
# UNFINISHED: see verify configuration func or whatever its called

import sys
import random

# evil global variables
max_iterations = 10000 # how many iterations the algorithm is allowed to go through before it declares it as failed
number_of_strings_to_test_on = 2 # how many strings the algorithm will be tested on
window_size = 6 # for now t = w

class algorithm:
    def __init__(self):
        self.rules = {}

    def add_rule(self, int, str):
        self.rules[int] = str


# utitlity functions:

# shuffles a string
def shuffle(string):
    return ''.join(random.sample(string,len(string)))

# partitions a string, allows shifting
def partition_string(str, window_size: int, shift: int):
    partitions = []
    for i in range(0, len(str), window_size):
        partitions.append(str[i+shift:i+window_size+shift])

    # add the beginning of the string to the last partition
    partitions[-1] += (str[:shift])
    return partitions

# returns the period of a string, if any
def principal_period(s):
    i = (s+s).find(s, 1, -1)
    return None if i == -1 else s[:i]

# finds all cyclic shifts of a string
def cyclic_shifts(string):
    cyclic_shifts_list = []
    if len(string) == 1:
        return [string]
    else:
        for char in string:
            string = ''.join([string[1:],string[0]])
        cyclic_shifts_list.append(string)
    return cyclic_shifts_list


#tests an algorithm on a specific string. returns true if the string eventually reached a valid conf, false if not
def test_algorithm_on_a_string(str, algorithm, num_of_max_iterations: int, window_size: int):
    shift = 0
    for i in range(0, max_iterations):
        shift = (shift + 1) % window_size
        partitions = partition_string(str, window_size, shift)
        for partition in partitions:
            count = partition.count('0')
            if count in algorithm.rules:
                partition = algorithm.rules[count]
        if verify_configuration_validity("".join(partitions)):
            print("succeeded!")
            print(partitions)
            return true
    return false


# verifies if the string is valid, used by test_algorithm
def verify_configuration_validity(string, valid_period):
    period_shifts = cyclic_shifts(valid_period)
    string_period = principal_period(string)
    for valid in period_shifts:
        if string_period == valid: return True
        if string_period == valid[::-1]: return True # if same as inversed period


def main():
    # input: [#R_rule_1] [pattern_rule_1] [#R_rule_2] [pattern_rule_2]

    if len(sys.argv) != 5:
        print('Error: incorrect number of rules given.')
        sys.exit(0)
    else:

        alg = algorithm()
        alg.add_rule(int(sys.argv[1]), sys.argv[2])
        alg.add_rule(int(sys.argv[3]), sys.argv[4])

        string = "0"*window_size + "1"*window_size
        valid_period = principal
        valid = 0
        for i in range(0, number_of_strings_to_test_on):
            print('testing on string: ' + string)
            string = shuffle(string)
            if test_algorithm_on_a_string(string, alg, max_iterations, window_size): valid += 1


main()
