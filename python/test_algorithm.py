# tests a given algo on a given input string, tries to reach a given pattern.
# input: [#0_rule_1] [pattern_rule_1] [#0_rule_2] [pattern_rule_2] [pattern to be reached] [input string] [max_iterations] [verbose]

# assumes the length of the pattern is also the window size. in other words, assumes w = t

import sys
import random
import algo
from committee import Committee
from configuration import configuration, configuration_builder

# utitlity functions:
#tests an algo on a specific string. returns True if the string eventually reached a valid conf, False if not
def test_algo_on_a_committee(conf: configuration):
    shift = -1 # so that it starts at 0
    past_configurations = []
    cycle_counter = 0
    used_max_iterations = True

    for i in range(0, conf.max_iterations):
        local_cycle = False
        shift = (shift + 1) % len(conf.committee)
        partitions = partition_committee(conf.committee, conf.window_size, shift)

        if verify_configuration_validity(conf):
            used_max_iterations = False
            break

        # checking for cycles
        if check_for_cycle(conf, past_configurations):
           local_cycle = True
           cycle_counter += 1

        if cycle_counter >= len(conf.expected_output):
            used_max_iterations = False
            print('assuming we\'ve reached full cycle. You should check this with verbose on! Algorithm: '
                    + str(conf.alg.rules) + " on string " + conf.committee)
            break
        #print(local_cycle)
        if local_cycle:
            if conf.verbose: print("cycle counter: " + str(cycle_counter))
            continue # already saw this configuration, shifting by one to check for other algo checks
        # no cycle detected, resetting.
        cycle_counter = 0

        # shifting chars in partitions according to the rules of the algo
        for i in range(0, len(partitions)):
            count = partitions[i].count('0')
            if count in conf.alg.rules:
                partitions[i] = conf.alg.rules[count]

        conf.committee = "".join(partitions)
        print(conf.committee)
        if(conf.verbose): print(conf.committee)

        if verify_configuration_validity(conf):
            used_max_iterations = False
            break
        else: past_configurations.append(conf.committee)
    if used_max_iterations: print(str(conf.alg.rules) + " needed more iterations on string input " + conf.committee)


# verifies if the string is valid, used by test_algo
def verify_configuration_validity(conf: configuration):
    valid = False
    partitions = []
    for i in range(0, conf.window_size):
        partitions = partition_committee(conf.committee, conf.window_size, i)
        count = [partition.count('0') for partition in partitions]
        if len(set(count)) == 1: # every partition has the same number of 0s, so string must be balanced.
            valid = True
            break
    if valid:
        if(conf.verbose): print("".join(partitions) + ": VALID")
        print(str(conf.alg.rules) + " succeeded!")
        return True
    return False


def main():
    if len(sys.argv) != 9:
        print('Error: incorrect number of inputs given: ' + str(sys.argv))
        sys.exit(0)

    alg = algo.algo(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4])
    cb = configuration_builder()
    conf = cb.with_alg(alg).with_pattern(sys.argv[5]).with_committee(sys.argv[6]).with_max_iterations(sys.argv[7]).with_verbose(sys.argv[8]).build()
    if conf is None:
        print('something went wrong with your configuration! Exiting.')
        sys.exit(0)

    if conf.verbose:
        print("testing " + str(conf.alg.rules) + " on " + conf.committee)

    test_algo_on_a_committee(conf)


# don't call main unless the script is called directly.
if __name__ == '__main__':
    main()
