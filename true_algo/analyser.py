# for figuring out how many rounds it should take.
import logging
import math

from circular_list import circular_list
from functools import reduce

# observer on configuration
class analyser:
    def __init__(self, p: str):
        self.p = p  # pattern
        self.pl = len(self.p)
        self.pz = p.count('0') # number of zeroes in p
        self.min_slices_per_rob = math.floor( self.pl / self.pz)

        #self.upper_bound = self.k + math.ceil(self.i * self.k / self.min_slices_per_rob)

    def count_invalid(self, c: str):
        slices = [c[i: i + self.pl] for i in range(0, len(c), self.pl)]
        count = 0
        for s in slices:
            if s.count('0') != self.pz:
                count += 1
        return count

    def verify_pass(self, old_c: str, new_c: str, rob: int):  # old config, new config, number of robots
        # verifies if the pass meets the bound, returns False if it does not
        old_i = self.count_invalid(old_c)
        new_i = self.count_invalid(new_c)
        valid_slices_made_this_pass = old_i - new_i
        min_valid_slices_to_have_made = min(self.min_slices_per_rob * rob, old_i);

        if not valid_slices_made_this_pass >= min_valid_slices_to_have_made:
            return False
        return True

    def analyse_excess_zeros(self, c: str):
        slices = [c[i: i + self.pl] for i in range(0, len(c), self.pl)]
        excess_zeroes = 0
        cumulative_excess_zeroes = []
        for s in slices:
            excess_zeroes += s.count('0') - self.pz
            cumulative_excess_zeroes.append(excess_zeroes)
