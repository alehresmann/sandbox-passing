# tests a given algo on a given input string, tries to reach a given pattern.
# input: [#0_rule_1] [pattern_rule_1] [#0_rule_2] [pattern_rule_2] [pattern to be reached] [input string] [max_iterations] [verbose]

# assumes the length of the pattern is also the window size. in other words, assumes w = t

import sys
import random
import algo
from committee import committee
from configuration import configuration, configuration_builder

# utitlity functions:
#tests an algo on a specific string. returns True if the string eventually reached a valid conf, False if not
def linear_algorithm(conf: configuration):
    for iteration in range(0, conf.max_iterations):
        if conf.verbose:
            print("starting " + str(iteration) + ":\t" + conf.c.get())
        if conf.c.is_valid():
            return True

        for rule in conf.alg.rules.values():
            valid_partitions = conf.c.get_partition_indices_which_can_apply_rule(rule)
            for index in valid_partitions:
                if conf.verbose:
                    print("Applying rule " + rule + " to partition " + str(index))
                conf.c.apply_rule(index, rule)
                if conf.c.is_valid():
                    return True

        if not conf.no_cycles and conf.c.is_cycle():
            if conf.verbose:
                print("Algo " + str(conf.alg.rules.values())[11:] + " has cycled: " + conf.c.get())
            return False
        if not conf.no_cycles:  # don't record cycles if no_cycles is .
            conf.c.record_partition()
        conf.c.shift(1)
    return False
