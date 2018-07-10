# tests a given algo on a given input string, tries to reach a given
# pattern.
# input: [#0_rule_1] [pattern_rule_1] [#0_rule_2] [pattern_rule_2]
# [pattern to be reached] [input string] [max_iterations] [verbose]

# assumes the length of the pattern is also the window size. in other
# words, assumes w = t

import sys
import random
import logging
from itertools import chain, combinations

from committee import committee
from committee_handler import committee_handler, handler_builder
from grapher import graph_tree

# tests an algo on a specific string. returns True if the string
# eventually reached a valid conf, False if not
def linear_algorithm(h: committee_handler, alg: list, c: committee):

    to_do_committees = {} #  dictionary of committees
    past_committees =  {} #  dictionary of committees

    logging.info('beginning computation: alg: ' + str(alg) + ' on ' + str(c))
    c.colour = 0  # beginning
    #past_committees[str(c)] = c.copy()

    for i in range(0, h.max_iterations):

        logging.debug(str(i) + ':\t' + str(c))

        if c.is_valid(h.pattern):
            if h.generate_image:
                c.colour = 2  # end
                past_committees[str(c)] = c.copy()
                graph_tree(h, past_committees)
            return True

        valid_partitions = c.get_partition_indices_which_can_apply_alg(alg)
        logging.debug('Applying alg to partitions '
                           + str(valid_partitions))
        c = h.apply_alg_to_committee(c, valid_partitions, alg)
        logging.debug('alg applied:\t' + str(c))

        if h.check_cycles and h.is_in_list(c, past_committees):
            return False

        if c.is_valid(h.pattern):
            if h.generate_image:
                c.colour = 2  # end
                past_committees[str(c)] = c.copy()
                graph_tree(h, past_committees)
            return True

        # don't record cycles if check_cycles is False
        if h.check_cycles:
            past_committees[str(c)] = c.copy()
        logging.debug('shifting')
        c = h.shift_committee(c, 1)

    if h.generate_image:
        graph_tree(h, past_committees)
    return False

# utility function for obtaining a powerset:
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def DFS_valid(h: committee_handler, c: committee):
    if c.is_valid(h.pattern):
        if not h.valid:
            h.valid = True
            h.valid_committee = str(c)
            if not h.full_tree:
                return True
    return False

# IDEA: have some queue to look at. every time one reaches some particular configuration, compute all possible configs, push them to the queue, then add that config to some list of 'done'. Then look at all configs in the list and repeat. if one reaches at some point. some config that's in the done list, then dont add it to the queue. make class 'comittee' wherein one has an ID and knows the ID of its parent, that way a path can be outputted
def DFS_algorithm(h: committee_handler, alg: list, initial: committee):

    to_do_committees = {} #  dictionary of committees
    past_committees =  {} #  dictionary of committees

    initial.colour = 0  # beginning
    to_do_committees[str(initial)] = initial.copy()
    committee_count = 0

    while (len(to_do_committees) > 0 and committee_count < h.max_iterations):
        committee_count += 1
        key, c = to_do_committees.popitem()
        logging.debug('iteration ' + str(committee_count) + '\t, on: ' + c.print_nicely() + ' parent: ' + str(c.parent))

        if DFS_valid(h, c):
            if h.generate_image:
                c.colour = 2
                past_committees[str(c)] = c.copy()
                graph_tree(h, past_committees)

            return True

        past_committees[str(c)] = c.copy()

        valid_partitions = c.get_partition_indices_which_can_apply_alg(alg)
        pset = list(powerset(valid_partitions))[1:]  # note: ignoring the first possibility, an empty set, as it wouldnt change the config
        logging.debug('found ' + str(len(pset)) + ' total possibilities of algorithm application')
        logging.debug(pset)
        for possibility in pset:
            new = committee(c.configuration, c.window_size, str(c))
            new = h.apply_alg_to_committee(new, possibility, alg)

            if not h.is_in_list(new, past_committees) and not h.is_in_list(new, to_do_committees):
               to_do_committees[str(new)] = new.copy()

        shifted = h.shift_committee(c, 1)
        shifted.reached_by = 'shifted'
        shifted.parent = c.print_nicely()
        if not h.is_in_list(shifted, past_committees) and not h.is_in_list(shifted, to_do_committees):
            logging.debug('shifting: ' + str(shifted))
            to_do_committees[str(shifted)] = shifted.copy()
    if committee_count == h.max_iterations:
        logging.warning('ran out of iterations. Increase max iterations count with -mi')
    if h.generate_image:
        graph_tree(h, past_committees)
    return h.valid
