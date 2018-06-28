import sys
import logging
from bitarray import bitarray
from committee import committee


class committee_handler:
    def __init__(self, pattern: str, max_iterations: int, verbose: bool, check_cycles: bool, check_shifts: bool):
        self.pattern = pattern
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.check_cycles = check_cycles
        self.check_shifts = check_shifts

        self.to_do_committees = set()
        self.past_committees = set()

    def _get_shifted_bitarray(self, arr: bitarray, shift_by: int):
        return bitarray(arr[shift_by:] + arr[:shift_by])

    def shift_committee(self, c: committee, shift_by: int) -> committee:
        config = self._get_shifted_bitarray(c.configuration, shift_by)
        return committee(config, c.window_size, c.identifier + 1, c.identifier)

    def _apply_rule_to_bitarray(self, arr: bitarray, partition_index: int, rule: str):
        window_size = len(rule)
        config = bitarray()
        config.extend(arr[:partition_index * window_size])
        config.extend(bitarray(rule))
        config.extend(arr[(partition_index + 1) * window_size:])
        return config

    def apply_alg_to_committees(self, c: committee, partition_indices: list, alg: list):
        new = committee(c.configuration, c.window_size, c.identifier + 1, c.identifier)
        for index in partition_indices:
            partition = new.get_partition(index) # the length of the rule is the window size
            for rule in alg:
                if partition.count(0) == rule.count('0'):
                    new.configuration = self._apply_rule_to_bitarray(new.configuration, index, rule)
        return new

    def _bitarrays_equals(self, config: bitarray, other: bitarray, window_size: int):
        # note: this checks if the current configuration and a given locked partition, stored as an int,
        # are the same in relation to their partitions: as in if, after having been partitioned, they
        # are a cyclic shifts of their PARTITIONS, not the strings within their partitions themselves.
        for i in range(0, len(config), window_size):
            if (config[i:] + config[:i]) == other:
                return True
        #print(str(config)[10:-2] + ' not eq to ' + str(other)[10:-2])
        return False

    def is_in_past(self, c: committee):
        configs = [committee.configuration for committee in self.past_committees]
        for past in self.past_committees:
            if self._bitarrays_equals(c.configuration, past.configuration, len(self.pattern)):
                logging.info('cycle:\t' + str(c) +' already reached at ' + str(past.identifier + 1))
                return True
        return False

    def clear(self):
        self.to_do_committees.clear()
        self.past_committees.clear()

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

    def build(self):
        if self.pattern is None or self.max_iterations == 0:
            return None
        return committee_handler(self.pattern, self.max_iterations, self.verbose, self.check_cycles, self.check_shifts)
