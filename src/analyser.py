# for figuring out how many rounds it should take.
import math


# observer on configuration
class analyser:
    def __init__(self, c: str, p: str):
        self.c = c  # configuration
        self.p = p  # pattern
        self.k = int(len(c) / len(p))
        self.i = self.count_invalid(c)
        self.m = math.floor(len(p) / p.count("0"))

        self.upper_bound = self.k + math.ceil(self.i * self.k / self.m)

        self.valid_slices_made_this_pass = 0

    def count_invalid(self, c: str):
        slices = [c[i : i + len(self.p)] for i in range(0, len(c), len(self.p))]
        count = 0
        for s in slices:
            if s.count("0") != self.p.count("0"):
                count += 1
        return count

    def get_upper_bound(self):
        return self.upper_bound

    def analyse_end_of_round(self, new_c: str, r: int):  # config, round
        # verifies if the pass meets the bound, returns False if it does not
        new_i = self.count_invalid(new_c)
        self.valid_slices_made_this_pass += self.i - new_i

        # I am at the end of the pass. Have I met my bound?
        if r > self.k and r % (self.k) == 0:
            if not self.valid_slices_made_this_pass >= self.m:
                return False
            else:
                self.valid_slices_made_this_pass += self.i - new_i

        self.c = new_c
        self.i = new_i
        return True

    def count_excess_zeros(self, c: str):
        slices = [c[i : i + len(self.p)] for i in range(0, len(c), len(self.p))]
        excess_zeroes = 0
        cumulative_excess_zeroes = []
        for s in slices:
            excess_zeroes += s.count("0") - self.p.count("0")
            cumulative_excess_zeroes.append(excess_zeroes)
        return cumulative_excess_zeroes
