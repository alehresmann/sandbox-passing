### for generating all plausible algorithms

import sys
import itertools

def main():
    if len(sys.argv) < 2:
        print("You must give me a string length before I can generate the algorithms!")
        sys.exit(0)
    else:

        # generate all binary strings of given length, but remove the one with only 0s and the one with only 1s
        binary_strings = ["".join(seq) for seq in itertools.product("01", repeat= int(sys.argv[1]))]
        binary_strings.remove("0"*int(sys.argv[1]))
        binary_strings.remove("1"*int(sys.argv[1]))

        combinations = itertools.combinations(binary_strings, 2)
        algorithms = []
        for comb in combinations:
            if comb[0].count('0') == comb[1].count('0'):
                continue
            algorithms.append( str(comb[0].count('0')) + " " + comb[0] + " " + str(comb[1].count('0')) + " " + comb[1])

        for alg in algorithms:
            print(alg)
main()
