import sys
import random
import itertools
import numpy as np

from algo import algo
import test_algorithm as ta


# bracelet generation functions
def binary_words(zeros, ones):
    n = zeros + ones
    for c in itertools.combinations(range(n), ones):
        word = np.zeros(n, dtype=int)
        word[list(c)] = 1
        yield tuple(word)


def cyclic_permute(word):
    for i in range(len(word)):
        yield word[i:] + word[:i]


def dihedral_permute(word):
    return itertools.chain(cyclic_permute(word), cyclic_permute(word[::-1]))


def is_reduced(word):
    return all(word <= w for w in dihedral_permute(word))


def balanced_bracelets(length):
    return list(filter(is_reduced, binary_words(length, length)))


def strings_balanced_bracelets(length):
    if not length % 2 == 0:
        print('Error string_balanced_nacklaces(length) in generators.py,'
              ' length must be even.')
        return None
    return [''.join(map(str, bracelet))
            for bracelet in balanced_bracelets(length)]


# ALGORITHMS

# shuffles a string
def shuffle(string):
    return ''.join(random.sample(string, len(string)))


def generate_random_algorithm(num_of_rules=2, length_of_pattern=8):
    if not length_of_pattern % 2 == 0:
        print('Error generate_random_algorithms'
              '(num_of_rules, length_of_pattern) in generators.py,'
              ' n must be even.')
        return None
    default_string = '0' * int(length_of_pattern / 2)
    + '1' * int(length_of_pattern / 2)
    alg = algo()
    for i in range(0, num_of_rules):
        added = False
        while not added:
            rule_count = random.randint(1, length_of_pattern - 1)
            if rule_count in alg.rules:
                continue
            else:
                alg.add_rule(shuffle('0' * rule_count
                             + '1' * (length_of_pattern - rule_count)))
            added = True
    return alg


def generate_all_algorithms(num_of_rules=2, length_of_pattern=8):
    binary_strings = [''.join(seq) for seq in
                      itertools.product('01', repeat=length_of_pattern)]
    binary_strings.remove('0' * length_of_pattern)
    binary_strings.remove('1' * length_of_pattern)

    algorithms = []
    combination = itertools.combinations(binary_strings, num_of_rules)
    for comb in combination:
        rules_count = [rule.count('0') for rule in comb]
        # all rules deal with different number of 0s
        if len(rules_count) == len(set(rules_count)):
            alg = algo()
            for rule in comb:
                alg.add_rule(rule)
            algorithms.append(alg)
    return algorithms


# MAIN
def main():
    if len(sys.argv) < 2:
        print('You need to give me some sort of generating guidance.'
              ' Check the file to see all possible choices.')
        sys.exit(0)
    generator = sys.argv[1]
    arg_1 = ''
    arg_2 = ''
    if len(sys.argv) > 2:
        arg_1 = sys.argv[2]
    if len(sys.argv) > 3:
        arg_2 = sys.argv[3]

    if generator == 'random_alg':
        if arg_2 != '':
            print(str(generate_random_algorithm(int(arg_1), int(arg_2))))
        else:
            print(str(generate_random_algorithm()))

    elif generator == 'all_alg':
        if arg_2 != '':
            [print(alg) for alg
             in generate_all_algorithms(int(arg_1), int(arg_2))]
        else:
            [print(alg) for alg in generate_all_algorithms()]

    elif generator == 'bracelets':
        if arg_1 != '':
            [print(bracelet) for bracelet
             in strings_balanced_bracelets(int(int(arg_1)/2))]
        else:
            [print(bracelet) for bracelet in strings_balanced_bracelets(4)]

    elif generator == 'binary_string':
        if arg_1 != '':
            [print(''.join(seq)) for seq
             in itertools.product('01', repeat=int(arg_1))]
        else:
            [print(''.join(seq)) for seq in itertools.product('01', repeat=8)]

    elif generator == 'string_permutations':
        if arg_1 != '':
            [print(''.join(seq)) for seq
             in set(itertools.permutations('0' * int(int(arg_1)/2))
             + '1' * int(int(arg_1) / 2))]
        else:
            [print(''.join(seq)) for seq
             in set(itertools.permutations('0' * 4 + '1' * 4))]

    elif generator == 'random_string':
        length = 8
        if arg_1 != '':
            length = int(arg_1)
        print(shuffle('0' * int(length / 2) + '1' * int(length / 2)))

    else:
        print('Didn\'t understand your input. check the file for options!')


# don't call main unless the script is called directly.
if __name__ == '__main__':
    main()
