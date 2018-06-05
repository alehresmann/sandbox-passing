import sys
import algo

class configuration:
    def __init__(self, alg: algorithm, pattern: str, input_string: str, expected_output: str, max_iterations: int, window_size: int, verbose: bool):
        self.alg = alg
        self.pattern = pattern
        self.input_string = input_string
        self.expected_output = expected_output
        self.max_iterations = max_iterations
        self.window_size = window_size
        self.verbose = verbose


class configuration_builder:
    def __init__(self):
        self.alg = None
        self.pattern = ""
        self.input_string = ""
        self.max_iterations = 0
        self.window_size = 0
        self.verbose = False

    def with_alg(self, alg: algorithm):
        self.alg = alg
        return self

    def with_pattern(self, pattern: str):
        self.pattern = pattern
        self.window_size = len(pattern)
        return self

    def with_input_string(self, input_string: str):
        self.input_string = input_string
        return self

    def with_max_iterations(self, max_iterations: int):
        self.max_iterations = int(max_iterations) # for some reason reads as a string so need to cast it
        return self

    def with_verbose(self, verbose: bool):
        self.verbose = (int(verbose) == 1)
        return self

    def build(self):
        if self.alg == None or self.pattern == "" or self.input_string == "" or self.max_iterations == 0:
            return None

        if len(self.input_string) % len(self.pattern) != 0:
            return None
        else:
            multiplier = int( len(self.input_string) / len(self.pattern))
            self.expected_output = self.pattern * multiplier

        return configuration(self.alg, self.pattern, self.input_string, self.expected_output, self.max_iterations, self.window_size, self.verbose)


