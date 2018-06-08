import sys
import struct
from bitarray import bitarray


# utility functions
def is_rotation_of(arr1: bitarray, arr2: bitarray):
    if len(arr1) != len(arr2):
        return False
    if (arr1 + arr1).search(arr2, 1):
        return True
    return False

def shift(string, shift_by: int):
        return string[shift_by:] + string[:shift_by]

class committee:
    def __init__(self, initial_config: str, pattern: str):
        if len(initial_config) % len(pattern) != 0:
            print('error! length of committee isn\'t a multiple of it\'s'
                  ' window size. Committee: ' + initial_config
                  + ', window_size ' + len(pattern))
            sys.exit('0')

        self.configuration = bitarray(initial_config)
        self.window_size = len(pattern)
        self.pattern = pattern
        self.past_iterations = set()

    def get(self):
        return str(self.configuration)[10:-2]

    def get_partition(self, index: int):
        return self.configuration[index
                * self.window_size: (index + 1) * self.window_size]

    def get_partitions(self):
        partitions = []
        for i in range(0, self.window_size):
            partitions.append(self.get_partition(i))
        return partitions

    def is_valid(self):
        # note: this function merely checks if all partitions do have the pattern, for efficiency.
        # If this algorithm were implemented in a truly distributed, one would need to do O(n)
        # step, wherein all partitions shift through the entire string and verify its validity.
        # they would hence all know they are valid.
        temp = self.configuration.copy()
        for i in range(0,self.window_size):
            temp = self.configuration[i:] + self.configuration[:i]
            valid = True
            for j in range(0, len(temp), self.window_size):
                if not str(temp[j:j+self.window_size])[10:-2] == self.pattern:
                    valid = False
            if valid:
                return True
        return False

    def shift(self, shift_by: int):
        # shifts the configuration by shift_by to the left
        self.configuration = shift(self.configuration, shift_by)

    def get_partition_indices_which_can_apply_rule(self, rule: str):
        # returns the indices of partitions which are allowed to apply the given rule.
        # that is, if the partition has the same number of 0s, but not if the partition
        # is a cyclic shift of the string. For example, for the rule 000111, the string
        # 010101 would be able to apply the given rule, but not 001111 and not 111000
        rule_count = rule.count('0')
        valid = []
        for i, partition in enumerate(self.get_partitions()):
            if partition.count(0) == rule_count:
                # ensuring partition isnt a rotation of the pattern
                #if not is_rotation_of(partition, bitarray(rule)):
                valid.append(i)
        return valid

    def apply_rule(self, partition_index: int, rule: str):
        new = bitarray()
        new.extend(self.configuration[:partition_index * self.window_size])
        new.extend(bitarray(rule))
        new.extend(self.configuration[(partition_index + 1) * self.window_size:])
        self.configuration = new

    def record_partition(self):
        current = 0
        for bit in self.configuration:  # NOTE: here too
            current = (current << 1) | bit

        self.past_iterations.add(current)

    def is_cycle(self):
        current = 0
        for bit in self.configuration:  # NOTE: here too
            current = (current << 1) | bit

        if current in self.past_iterations:
            return True
        return False

    def equals(self, other: int):
        # note: this checks if the current configuration and a given locked partition, stored as an int,
        # are the same in relation to their partitions: as in if, after having been partitioned, they
        # are a cyclic shifts of their PARTITIONS, not the strings within their partitions themselves.
        for i in range(0, len(self.configuration), self.window_size):
            temp = self.configuration[i:] + self.configuration[:i]
            temp_int = 0
            # NOTE: the loop below might be ineficcient
            for bit in temp:
                temp_int = (temp_int << 1) | bit

            if temp_int == other:
                return True
        return False
