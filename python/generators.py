import sys
from itertools import combinations, chain
import numpy as np

import algo
import test_algorithm as ta

# shuffles a string
#def shuffle(string):
#    return ''.join(random.sample(string,len(string)))

######  DISTINCT NECKLACES
# Takes an integer and returns all distinct 2n necklaces of that length. Strings are considered identical necklaces if:
# * they are a cyclic permutation of one another:                       e.g. 1010   == 0101
# * they are a mirroring of one another:                                e.g. 101100 == 001101
# * they are a cyclic permutation of a mirroring of one another:        e.g. 101100 == 011010

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
    if not n % 2 == 0:
        print("Error string_balanced_nacklaces(n) in generators.py, n must be even.")
        return None
    return [''.join(map(str,necklace)) for necklace in balanced_necklaces(n)]


##### ALGORITHMS
def generate_random_algorithm(num_of_rules = 2, length_of_pattern = 8):
    if not n % 2 == 0:
        print("Error generate_random_algorithms(num_of_rules, length_of_pattern) in generators.py, n must be even.")
        return None
    default_string = '0' * int(length_of_pattern / 2) + '1' * int(length_of_pattern / 2)
    alg = algo()
    for i in range(0, num_of_rules):
        added = False
        while not added:
            rule_count = randint(1,length_of_pattern - 1)
        if rules_count in alg.rules:
            continue
        else alg.add_rule(rule_count, shuffle('0' * rule_count + '1' * (length_of_pattern - rules_count)))
        added = True
    return alg

def generate_all_algorithms(num_of_rules = 2, length_of_pattern = 8):
    binary_strings = ["".join(seq) for seq in itertools.product("01", repeat= length_of_pattern)]
    binary_strings.remove("0" * length_of_pattern)
    binary_strings.remove("1" * length_of_pattern)

    algorithms = []
    combination = itertools.combinations(binary_strings, num_of_rules)
    for comb in algorithms:
        rules_count = [rule.count('0') for rule in comb]
        if len(rules_count) == len(set(rules_count)): # all rules deal with different number of 0s
            alg = algo()
            for rule in comb:
                alg.add_rule(str(rule.count('0'), rule))
            algorithms.append(alg)
    return algorithms


##### MAIN
def main():
    if len(sys.argv) != 2:
        print("You need to give me some sort of generating guidance. Check the file to see all possible choices.")
        sys.exit(0)
    generator = sys.argv[1]
    arg_1 = ""
    arg_2 = ""
    if len(sys.argv > 2): arg_1 = sys.argv[2]
    if len(sys.argv > 3): arg_2 = sys.argv[3]

    if   generator == "random":
        if arg_2 != "":
            print(generate_random_algorithm(int(arg_1), int(arg_2)))
        else: print(generate_random_algorithm())

    elif generator == "all":
        if arg_2 != "":
            [print(alg) for alg in generate_all_algorithms(int(arg_1), int(arg_2))]
        else: [print(alg) for alg in generate_all_algorithms()]

    elif generator == "necklaces":
        if arg_1 != "":
            [print necklace for necklace in strings_balanced_nacklaces( int(arg_1))]
        else: [print necklace for necklace in strings_balanced_nacklaces()]

    elif generator == "binary":
        if arg_1 != "":
            [print("".join(seq)) for seq in itertools.product("01", repeat = len(int(arg_1))]
        else:
           [print("".join(seq)) for seq in itertools.product("01", repeat = 8)]
    elif generator == "permutations":
        if arg_1 != "":
            [print("".join(seq)) for seq in set(itertools.permutations('0' * int(int(arg_1) / 2)) + '1' * int(int(arg_1) / 2)))]
        else:
            [print("".join(seq)) for seq in set(itertools.permutations('0' * 4 + '1' * 4)))]

# don't call main unless the script is called directly.
if __name__ == '__main__':
    main()
