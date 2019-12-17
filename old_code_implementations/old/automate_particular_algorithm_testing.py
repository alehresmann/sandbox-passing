# automatically tests randomly generated algorithms that should theoretically always works. Should change to test all permutations of working algorithms.

import os
import sys
import generate_all_particular_algorithms as gen

#all
algorithms = gen.generate_all_algorithms("000111")
for alg in algorithms:
    os.system("python3 test_some_algorithm.py " + alg + " 000111")

#random
#while(True):
#    alg = gen.generate_random_algorithm("000111")
#    os.system("python3 test_some_algorithm.py " + alg + " 000111")

