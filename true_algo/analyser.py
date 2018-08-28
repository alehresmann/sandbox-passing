# for figuring out how many rounds it should take.
import logging
import math
from circular_list import circular_list
from functools import reduce

class analyser:
    def __init__(self):
        pass
    def get_upper_bound(self, c: str, p: str):  # configuration, pattern

        i = self.count_invalid(c, p)
        k = int(len(c)/len(p))

        expected = (k - 1) + i * (k - 1) / 2
        if expected < k:
            expected = k
        return expected


    def count_invalid(self, c: str, p: str):
        slices = [c[i: i + len(p)] for i in range(0, len(c), len(p))]
        count = 0
        for s in slices:
            if s.count('0') != p.count('0'):
                count += 1
        return count

## currently unused but thought to have been useful at some point
def geometric_mean(seq):
    return reduce(lambda x, y: x*y, seq)**(1.0/len(seq))

def arithmetic_mean(seq):
    return float(sum(seq))/max(len(seq),1)

def main():
    ## tester
    a = analyser()
    a.analyse('000000000000111111111111','000111')
