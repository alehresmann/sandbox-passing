import sys
import logging
import numpy as np
import pandas as pd

from bitarray import bitarray
from committee import committee


class committee_handler:
    def __init__(self, pattern: str, max_iterations: int, verbose: bool,
            check_cycles: bool, check_shifts: bool, full_tree: bool, generate_image: bool):
        self.pattern = pattern
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.check_cycles = check_cycles
        self.check_shifts = check_shifts
        self.full_tree = full_tree
        self.generate_image = generate_image
        self.valid = False
        self.valid_committee = -1

    def _get_shifted_bitarray(self, arr: bitarray, shift_by: int):
        return bitarray(arr[shift_by:] + arr[:shift_by])

    def shift_committee(self, c: committee, shift_by: int) -> committee:
        config = self._get_shifted_bitarray(c.configuration, shift_by)
        new = committee(config, c.window_size, c.print_nicely())
        new.reached_by = 'shift'
        return new

    def _apply_rule_to_bitarray(self, arr: bitarray, partition_index: int, rule: str):
        window_size = len(rule)
        config = bitarray()
        config.extend(arr[:partition_index * window_size])
        config.extend(bitarray(rule))
        config.extend(arr[(partition_index + 1) * window_size:])
        return config

    def apply_alg_to_committee(self, c: committee, partition_indices: list, alg: list):
        new = committee(c.configuration, c.window_size, c.print_nicely())
        new.reached_by = 'alg on: ' + str(partition_indices)
        for index in partition_indices:
            partition = new.get_partition(index) # the length of the rule is the window size
            for rule in alg:
                # if partition has same num of 0s as in the rule but isnt exactly the same as the rule
                if partition.count(0) == rule.count(0):
                    new.configuration = self._apply_rule_to_bitarray(new.configuration, index, rule)
        return new

    def _bitarrays_equals(self, config: bitarray, other: bitarray, window_size: int):
        # note: this checks if the current configuration and a given locked partition, stored as an int,
        # are the same in relation to their partitions: as in if, after having been partitioned, they
        # are a cyclic shifts of their PARTITIONS, not the strings within their partitions themselves.
        for i in range(0, len(config), window_size):
            if (config[i:] + config[:i]) == other:
                return True
        return False

    def is_in_list(self, c: committee, cd: dict):  # cd = committee_dictionary
        rotations = c.get_all_equal_bitarrays()
        for rotation in rotations:
            if rotation.to01() in cd:
                #logging.info('cycle:\t' + c.print_nicely() +' already reached ')   #TODO
                return True
        return False

class handler_builder:
    def __init__(self):
        self.pattern = None
        self.max_iterations = 0
        self.verbose = False
        self.check_cycles = False
        self.check_shifts = False

    def with_pattern(self, pattern: str):
        self.pattern = pattern
        return self

    def with_max_iterations(self, max_iterations: int):
        self.max_iterations = max_iterations
        return self

    def with_verbose(self, verbose: bool):
        self.verbose = verbose
        return self

    def with_check_cycles(self, check_cycles: bool):
        self.check_cycles = check_cycles
        return self

    def with_check_shifts(self, check_shifts: bool):
        self.check_shifts = check_shifts
        return self

    def with_full_tree(self, full_tree: bool):
        self.full_tree = full_tree
        return self

    def with_generate_image(self, generate_image: bool):
        self.generate_image = generate_image
        return self

    def build(self):
        if self.pattern is None or self.max_iterations == 0:
            return None
        return committee_handler(self.pattern, self.max_iterations, self.verbose, self.check_cycles, self.check_shifts, self.full_tree, False)
