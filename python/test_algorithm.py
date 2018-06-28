# tests a given algo on a given input string, tries to reach a given
# pattern.
# input: [#0_rule_1] [pattern_rule_1] [#0_rule_2] [pattern_rule_2]
# [pattern to be reached] [input string] [max_iterations] [verbose]

# assumes the length of the pattern is also the window size. in other
# words, assumes w = t

import sys
import random
import logging

from committee import committee
from committee_handler import committee_handler, handler_builder


# tests an algo on a specific string. returns True if the string
# eventually reached a valid conf, False if not
def linear_algorithm(h: committee_handler, alg: list, c: committee):
    logging.info('beginning computation: alg: ' + str(alg) + ' on ' + str(c))
    for i in range(0, h.max_iterations):
        logging.debug(str(i) + ':\t' + str(c))

        if c.is_valid(h.pattern):
            return True
        valid_partitions = c.get_partition_indices_which_can_apply_alg(alg)
        logging.debug('Applying alg to partitions '
                           + str(valid_partitions))
        c = h.apply_alg_to_committees(c, valid_partitions, alg)
        c.identifier = i
        c.parent_id  = i - 1
        logging.debug('alg:\t' + str(c))

        if h.check_cycles and h.is_in_past(c):
            return False

        if c.is_valid(h.pattern):
            return True

        # don't record cycles if check_cycles is False
        if h.check_cycles:
            h.past_committees.add(c.copy())
        logging.debug('shifting')
        c = h.shift_committee(c, 1)
    return False

# utility function for obtaining a powerset:

def powerset(s):
    pset = []
    x = len(s)
    for i in range(1 << x):
        [print(s[j]) for j in range(x) if (i & (1 << j))]
    return pset

# IDEA: have some queue to look at. every time one reaches some particular configuration, compute all possible configs, push them to the queue, then add that config to some list of 'done'. Then look at all configs in the list and repeat. if one reaches at some point. some config that's in the done list, then dont add it to the queue. make class 'comittee' wherein one has an ID and knows the ID of its parent, that way a path can be outputted
def DFS_algorithm(h: committee_handler, alg: list, initial: committee):
    h.to_do_committees.add(initial)
    committee_count = 1
    while(len(h.to_do_committees) > 0 and committee_count < h.max_iterations):

        c = h.to_do_committees.pop()
        logging.debug('committee ' + str(c.identifier) +', parent: ' + str(c.parent_id) +'\t:  ' + str(c))
        if c.is_valid(h.pattern):
            return True

        valid_partitions = c.get_partition_indices_which_can_apply_alg(alg)
        print(valid_partitions)
        pset = powerset(valid_partitions)
        print(str(pset))
        logging.debug('found ' + str(len(pset)) + ' total possibilities')

        for possibility in pset:
            new = committee(c.configuration, c.window_size)
            new = h.apply_alg_to_committee(new, valid_partitions, alg)

            new.identifier =  committee_count
            committee_count += 1
            new.parent_id = c.identifier

            if h.check_cycles and h.is_cycle(new):
                continue

            if new.is_valid(h.pattern):
                logging.warning(str(new) + ', committee ' + str(new.identifier) + 'has reached the pattern!')
                return True

            h.to_do_committee.add(new)

        shifted = h.shift_committee(c, 1)
        shifted.identifier = committee_count
        committee_count += 1
        shifted.parent_id = c.identifier
        if h.check_cycles and not h.is_cycle(shifted):
            print('shifted:' + str(shifted))
            h.to_do_committees.add(new)

        h.record_committee_as_past(c)
    #print([ str(committee) for committee in setting.handler.past_committees])
    #print('\n\n')
    #print([ str(committee) for committee in setting.handler.to_do_committees])
    return False
