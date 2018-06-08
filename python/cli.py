# input:    [#0_rule_1] [pattern_rule_1] [#0_rule_2] [pattern_rule_2]
#           [pattern to be reached] [input string] [max_iterations]
#           [verbose]

# Assumes the length of the pattern is also the window size.
# In other words, assumes w = t

import sys
import argparse

from algo import algo
from committee import committee
from configuration import configuration, configuration_builder
import generators as gen
import test_algorithm as ta
import filereader as fr

def main():
    parser = argparse.ArgumentParser(description='CLI for testing'
                                    'schelling algorithms')
    # PATTERN
    parser.add_argument('pattern', type=str, default='00001111',
            help='The pattern that the algorithm will try to reach')


    # INPUT STRING
    # note: input_string and (multiplier, num_of_strings) should be
    # mutually exclusive, whilst (multiplier and num_of_strings) should
    # be mutually inclusive, if used. Python's argparse doesn't allow
    # this as of yet, so for now  it is dependent on the user

    # use this
    parser.add_argument('--input', '-i', type=str,
            help='The input string to test the algorithm(s) on.')

    # XOR these
    parser.add_argument('--multiplier', '-m', type=int,
            help='the multiplier of the randomly generated string')
    parser.add_argument('--random_strings','-rs', type=int, help='the'
        'number of strings to be randomly generated and tested upon')

    # XOR this
    parser.add_argument('--strings_file','-sf', type=str,
            help='the name of the file containing strings that must be'
            'tested')


    # ALGORITHM
    # use this
    parser.add_argument('--algorithm', '-a', type=str, nargs='+',
            help='the particular algorithm to test')

    # XOR these
    parser.add_argument('--num_of_random_algorithms', '-nra', type=int,
            help='the number of random algorithms to generate')
    parser.add_argument('--num_of_rules', '-nr', type=int,
            help='the number of rules for generating random algorithms')

    # XOR this
    parser.add_argument('--all_algorithms','-all', action='store_true')

    # XOR this
    parser.add_argument('--algorithms_file', '-af', help='runs all'
            ' algorithms contained in a given file')


    # CONFIGURATION
    # use all of these optionally
    parser.add_argument('--verbose', '-v', action='store_true',
            default=False, help='print information on every iteration')
    parser.add_argument('--max_iterations', '-mi', type=int,
            default=10000, help='the max iterations required before'
            ' the algorithm quits.')
    parser.add_argument('--no-cycles', '-nc',
            action='store_true', help='turns off checking for cycles.')

    # COMPUTE ARGS
    args = parser.parse_args()
    print(args)
    cb = configuration_builder().with_verbose(args.verbose)
    cb.with_max_iterations(args.max_iterations)
    cb.with_no_cycles(args.no_cycles)

    input_strings = []
    algorithms = []
    # verifying mutual exclusion and mutual inclusion for input_string
    # and algorithm input
    if not ((args.input is not None)
            ^ (args.multiplier is not None)
                and (args.random_strings is not None)
            ^ (args.strings_file is not None)):
        print('invalid string input! make sure to only use one of the'
                ' detailed input methods.')
        sys.exit(0)

    if not ((args.algorithm is not None)
            ^ (((args.num_of_random_algorithms is not None)
                and (args.num_of_rules is not None))
                or ((args.all_algorithms == True)
                    and (args.num_of_rules is not None)))
            ^ (args.algorithms_file is not None)):
        print('invalid algorithm input! make sure to only use one of'
        ' the detailed input methods.')
        sys.exit(0)

    # actually inputting input_string
    if args.input is not None:
        input_strings.append(args.input)
    elif (args.multiplier is not None
    and args.random_strings is not None):
        string = ('0'* args.pattern.count('0') + '1'
                * args.pattern.count('1'))
        string *= args.multiplier
        for i in range(0, args.random_strings):
            string = gen.shuffle(string)
            input_strings.append(string)
    elif args.strings_file is not None:
        input_strings = fr.readlines(args.strings_file)
    else:
        print('invalid string input! make sure to only use one of the'
                ' detailed input methods.')
        sys.exit(0)

    # actually inputting algorithms
    if args.algorithm is not None:
        alg = algo()
        for rule in args.algorithm:
            alg.add_rule(rule)
        algorithms.append(alg)
    elif ((args.num_of_random_algorithms is not None)
    and (args.num_of_rules is not None)):
        for i in range(0, args.num_of_random_algorithms):
            algorithms.append(gen.generate_random_algorithm(
                len(args.pattern), args.num_of_rules))
    elif args.all_algorithms and args.num_of_rules is not None:
        algorithms = gen.generate_all_algorithms(args.num_of_rules,
                len(args.pattern))
    elif args.algorithms_file:
        alg_strings = fr.readlines(args.algorithms_file)
        for alg_string in alg_strings:
            rules = alg_string.split()
            alg = algo()
            for rule in rules:
                alg.add_rule(rule)
            algorithms.append(alg)

    else:
        print('invalid algorithm input! make sure to only use one of '
        'the detailed input methods.')
        sys.exit(0)

    for alg in algorithms:
        valid = True
        for string in input_strings:
            cb.with_alg(alg)
            cb.with_committee(committee(string, args.pattern))
            conf = cb.build()
            if not ta.linear_algorithm(conf):
                valid = False
                break
        if valid:
            print("Algo " + str(conf.alg.rules.values())[11:]
                    + " succeeded ")

# don't call main unless the script is called directly.
if __name__ == '__main__':
    main()
