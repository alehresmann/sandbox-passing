### generates an algorithm that should theoretically always work for some particular given pattern.

import sys
import itertools
import random


def shuffle(string):
    return ''.join(random.sample(string,len(string)))


def generate_all_algorithms(pattern: str):
    rule_1 = pattern
    count_0_rule_1 = rule_1.count('0')
    binary_strings = ["".join(seq) for seq in itertools.product("01", repeat = len(pattern))]
    all_strings_with_equal_0s_as_rule_1 = set(["".join(seq) for seq in itertools.permutations(pattern)])
    for string in all_strings_with_equal_0s_as_rule_1:
        binary_strings.remove(string)

    algorithms = []
    for string in binary_strings:
        rule_2 = string
        count_0_rule_2 = rule_2.count('0')
        algorithms.append(str(count_0_rule_1) + " " + rule_1 + " " + str(count_0_rule_2) + " " + rule_2)
    return algorithms



def generate_random_algorithm(pattern: str):
    rule_1 = pattern
    count_0_rule_1 = rule_1.count('0')
    count_0_rule_2 = count_0_rule_1 # to keep the while loop going initially
    # generate some rule count randomly that isn't the same as rule 1
    while(count_0_rule_2 == count_0_rule_1):
        count_0_rule_2 = random.randint(1, len(rule_1) - 1)
    rule_2 = '0'* count_0_rule_2 + '1' * ( len(rule_1) - count_0_rule_2)
    rule_2 = shuffle(rule_2)
    return str( str(count_0_rule_1) + " " + rule_1 + " " + str(count_0_rule_2) + " " + rule_2)

