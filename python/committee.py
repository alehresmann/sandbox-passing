import sys
import struct

from bitarray import bitarray


class committee:
    # Committees are composed of a bitarray, an id, and a parent id. They are assumed to be never changing,
    # hence all functions on here perform checks, not modifications (beyond the initial setup)
    # for (modifying) creating a new committee from an old one, see committee_handler.
    def __init__(self, initial_config, window_size, identifier=0, parent_id=-1):
        self.identifier  = identifier
        self.parent_id   = parent_id
        self.window_size = window_size
        if isinstance(initial_config, str):
            self.configuration = bitarray(initial_config)
        else:
            self.configuration = initial_config.copy()

    def __str__(self):
        ret = ''
        string = str(self.configuration)[10:-2]
        for i in range(0, len(self.configuration), self.window_size):
            ret +=  string[i: i + self.window_size] + ','
        return ret

    def get(self) -> bitarray:
        return self.configuration

    def get_partition(self, index: int) -> bitarray:
        return self.configuration[index * self.window_size: (index + 1)
                * self.window_size]

    def get_partitions(self) -> list:  # list[bitarray]
        partitions = []
        for i in range(0, self.window_size):
            partitions.append(self.get_partition(i))
        return partitions

    def is_valid(self, pattern: str): #TODO: implement this in a distributed manner
        # note: this function merely checks if all partitions do have
        # the pattern, for efficiency.
        # If this algorithm were implemented in a truly distributed,
        # one would need to do an O(n) step, wherein all partitions
        # shift through the entire string and verify its validity.
        # they would hence all know they are valid.
        if len(pattern) != self.window_size:
            return False

        temp = self.configuration.copy()
        for i in range(0, self.window_size):
            temp = self.configuration[i:] + self.configuration[:i]
            valid = True
            for j in range(0, len(temp), self.window_size):
                if not str(temp[j:j+self.window_size])[10:-2] == pattern:
                    valid = False
            if valid:
                return True
        return False

    def _is_rotation_of(self, arr1: bitarray, arr2: bitarray):
        if len(arr1) != len(arr2):
            return False
        if (arr1 + arr1).search(arr2, 1):
            return True
        return False

    def get_partition_indices_which_can_apply_alg(self, alg : list, check_shifts = False):
        # returns the indices of partitions which are allowed to apply
        # the given rule. that is, if the partition has the same number
        # of 0s, but not if the partition is a cyclic shift of the
        # string. For example, for the rule 000111, the string 010101
        # would be able to apply the given rule, but not 001111 and not
        # 111000
        partitions = []

        for rule in alg:
            rule_count = rule.count('0')
            for i, partition in enumerate(self.get_partitions()):
                if partition.count(0) == rule_count:
                    # ensuring partition isnt a rotation of the pattern
                    if ((not check_shifts)
                            or (not is_rotation_of(partition, bitarray(rule)))):
                        partitions.append(i)
        return partitions

    def copy(self):
        return committee(self.configuration, self.identifier, self.parent_id)
