# tests a particular algorithm on distinct necklaces.

import sys
import random
from generate_all_distinct_necklaces import strings_balanced_necklaces


# evil global variables
max_iterations = 1000000 # how many iterations the algorithm is allowed to go through before it declares it as failed
number_of_strings_to_test_on = 100 # how many strings the algorithm will be tested on
window_size = 6 # for now t = w
num_of_times_to_repeat_pattern = 3

class algorithm:
    def __init__(self):
        self.rules = {}

    def add_rule(self, int, str):
        self.rules[int] = str


# utitlity functions:

# shuffles a string
def shuffle(string):
    return ''.join(random.sample(string,len(string)))

# partitions a string, allows shifting
def partition_string(str, window_size: int, shift: int):
    partitions = []
    str = str[shift:] + str[:shift]
    for i in range(0, len(str), window_size):
        partitions.append(str[i:(i+window_size)])

    return partitions

# returns the period of a string, if any
def principal_period(s):
    i = (s+s).find(s, 1, -1)
    return None if i == -1 else s[:i]

# finds all cyclic shifts of a string
def cyclic_shifts(string):
    cyclic_shifts_list = []
    if len(string) == 1:
        return [string]
    else:
        for char in string:
            string = ''.join([string[1:],string[0]])
        cyclic_shifts_list.append(string)
    return cyclic_shifts_list

#tests an algorithm on a specific string. returns true if the string eventually reached a valid conf, false if not
def test_algorithm_on_a_string(input_string: str,output_string: str, alg: algorithm, num_of_max_iterations: int, window_size: int):
    shift = -1 # so that it starts at 0
    past_configurations = []

    for i in range(0, max_iterations):
        shift = (shift + 1) % len(input_string)
        partitions = partition_string(input_string, window_size, shift)

        for i in range(0, len(partitions)):
            count = partitions[i].count('0')
            if count in alg.rules:
                partitions[i] = alg.rules[count]

        current = "".join(partitions)
        print(partitions)
        # checking for cycles
        for past in past_configurations:
            if current == past:
                return "cycle"

        if verify_configuration_validity(current, partitions, output_string):
            print(current + ": VALID")
            return "reached"
        else:
            past_configurations.append(current)
    return "max iterations"

# verifies if the string is valid, used by test_algorithm
def verify_configuration_validity(current: str, partitions: list, expected_output):
    actual_period = principal_period(current)
    #print(actual_period)
    if actual_period != None:
        expected_period = principal_period(expected_output)
        expected_period_shifts = cyclic_shifts(expected_period)
        for shift in expected_period_shifts:
            if shift == actual_period: return True
            if shift == actual_period[::-1]: return True # if same as inversed period

    for partition in partitions:
        if partition.count('0') != partition.count('1'): return False

    return True


def main():
    # input: [#0_rule_1] [pattern_rule_1] [#0_rule_2] [pattern_rule_2] [pattern to be reached] [input string]
    if len(sys.argv) != 7:
        print('Error: incorrect number of inputs given: ' + str(sys.argv))
        sys.exit(0)

    else:

        alg = algorithm()
        alg.add_rule(int(sys.argv[1]), sys.argv[2])
        alg.add_rule(int(sys.argv[3]), sys.argv[4])
        pattern =  sys.argv[5]
        #print("testing " + str(alg.rules))
        #expected_outputs = strings_balanced_necklaces(int(window_size/2)) # note: function is from generate_all_distinct_necklaces.py
        #for i in range(0, len(expected_outputs)):
        #    expected_outputs[i] = expected_outputs[i] * num_of_times_to_repeat_pattern

        expected_output = pattern * num_of_times_to_repeat_pattern

        succeeded = True
        for j in range(0, number_of_strings_to_test_on):
            random_input_string =  "010111111001100111000100011000" #shuffle(expected_output) #shuffle(expected_outputs[i])
            result = test_algorithm_on_a_string(random_input_string, expected_output, alg, max_iterations, window_size)
            if result == "max iterations":
                print(str(alg.rules) + " needed more iterations on string input " + random_input_string)
                succeeded = False
                break
            elif result == "cycle":
                print(str(alg.rules) + " cycled on " + random_input_string + " after " + str(j+ 1)  + " strings.")
                succeeded = False
                break
        if succeeded:
            print(str(alg.rules) + " succeeded!")
main()
