# tests a given algo on a given input string, tries to reach a given pattern.
# input: [#0_rule_1] [pattern_rule_1] [#0_rule_2] [pattern_rule_2] [pattern to be reached] [input string] [max_iterations] [verbose]

# assumes the length of the pattern is also the window size. in other words, assumes w = t

import sys
import random
import algo
import configuration

# utitlity functions:
# partitions a string, allows shifting
def partition_string(input_string: str, window_size: int, shift: int):
    input_string = input_string[shift:] + input_string[:shift]
    partitions = []
    for i in range(0, len(input_string), window_size):
        partitions.append(input_string[i:(i+window_size)])
    return partitions


# defined here so one can break out of a bigger loop that uses this function.
def check_for_cycle(partitions_as_single_string, past_configurations, verbose):
    for past in past_configurations:
        if partitions_as_single_string == past: return True
    return False

#tests an algo on a specific string. returns True if the string eventually reached a valid conf, False if not
def test_algo_on_a_string(conf: configuration):
    shift = -1 # so that it starts at 0
    past_configurations = []
    cycle_counter = 0
    used_max_iterations = True

    for i in range(0, conf.max_iterations):
        local_cycle = False
        shift = (shift + 1) % len(conf.input_string)
        partitions = partition_string(conf.input_string, conf.window_size, shift)

        if verify_configuration_validity(partitions, conf):
            used_max_iterations = False
            break

        partitions_as_single_string = "".join(partitions)
        # checking for cycles
        if check_for_cycle(partitions_as_single_string, past_configurations, conf.verbose):
            local_cycle = True
            cycle_counter += 1

        if cycle_counter >= len(conf.expected_output):
            print('assuming we\'ve reached full cycle. You should check this with verbose on! Algorithm: '
                    + str(conf.alg.rules) + " on string " + conf.input_string)
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

        partitions_as_single_string = "".join(partitions)
        if(conf.verbose): print(partitions_as_single_string)

        if verify_configuration_validity(partitions, conf):
            used_max_iterations = False
            break
        else: past_configurations.append(partitions_as_single_string)

    if used_max_iterations: print(str(conf.alg.rules) + " needed more iterations on string input " + conf.input_string)


# verifies if the string is valid, used by test_algo
def verify_configuration_validity(partitions: list, conf: configuration):
    for partition in partitions:
        if partition.count('0') != conf.pattern.count('0'): return False

    if(conf.verbose): print("".join(partitions) + ": VALID")
    print(str(conf.alg.rules) + " succeeded!")
    return True


def main():
    if len(sys.argv) != 9:
        print('Error: incorrect number of inputs given: ' + str(sys.argv))
        sys.exit(0)

    alg = algo(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4])

    cb = configuration_builder()
    conf = cb.with_alg(alg).with_pattern(sys.argv[5]).with_input_string(sys.argv[6]).with_max_iterations(sys.argv[7]).with_verbose(sys.argv[8]).build()
    if conf is None:
        print('something went wrong with your configuration! Exiting.')
        sys.exit(0)

    if conf.verbose:
        print("testing " + str(conf.alg.rules) + " on " + conf.input_string)

    test_algo_on_a_string(conf)


# don't call main unless the script is called directly.
if __name__ == '__main__':
    main()
