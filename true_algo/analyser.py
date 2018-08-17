# for figuring out how many rounds it should take.
import logging
import math
from circular_list import circular_list
from functools import reduce

class analyser:
    def __init__(self):
        pass
    def analyse(self, configuration: str, pattern: str):
        cl = circular_list(configuration)
        distances = []
        for i in range(0, len(cl)):
            current = cl.get_node_at(i)
            left = current
            left_counter = 0
            while left.data == current.data:
                left = left.prev
                left_counter += 1

            right = current
            right_counter = 0
            while right.data  == current.data:
                right = right.next
                right_counter += 1

            if right_counter > left_counter:
                distances.append(left_counter)
            else:
                distances.append(right_counter)

        print('arithmetic mean of distances: ', arithmetic_mean(distances))

def geometric_mean(seq):
    return reduce(lambda x, y: x*y, seq)**(1.0/len(seq))

def arithmetic_mean(seq):
    return float(sum(seq))/max(len(seq),1)

def main():
    ## tester
    a = analyser()
    a.analyse('000000000000111111111111','000111')

#        estimated_rounds = 0
#
#        zeros_blocks_length = []
#        ones_blocks_length = []
#        count = 0
#        last_bit = configuration[0]
#        for i in range(0, len(configuration)):
#            current = configuration[i]
#
#            if current == last_bit:
#                count += 1
#
#            if current != last_bit:
#                if last_bit == '1':
#                    ones_blocks_length.append(count)
#                else:
#                    zeros_blocks_length.append(count)
#                count = 1
#                last_bit = current
#
#            if i == len(configuration) - 1:
#                if current == '1':
#                    ones_blocks_length.append(count)
#                else:
#                    zeros_blocks_length.append(count)
#
#        gz = geometric_mean(zeros_blocks_length)  # average distance
#        go = geometric_mean(ones_blocks_length)
#        az = arithmetic_mean(zeros_blocks_length) # average length
#        ao = arithmetic_mean(ones_blocks_length)
#
#        estimated_rounds = (gz + go) / len(configuration)
#        print('z', gz, az, 'o', go, ao)
