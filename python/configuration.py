import sys
from algo import algo


class Configuration:
    def __init__(self, alg: algo, pattern: str, committee: str,
                 expected_output: str, max_iterations: int,
                 window_size: int, verbose: bool):
        self.alg = alg
        self.pattern = pattern
        self.committee = committee
        self.expected_output = expected_output
        self.max_iterations = max_iterations
        self.window_size = window_size
        self.verbose = verbose


class Configuration_builder:
    def __init__(self):
        self.alg = None
        self.pattern = ""
        self.committee = ""
        self.max_iterations = 0
        self.window_size = 0
        self.verbose = False

    def with_alg(self, alg: algo):
        self.alg = alg
        return self

    def with_pattern(self, pattern: str):
        self.pattern = pattern
        self.window_size = len(pattern)
        return self

    def with_committee(self, committee: str):
        self.committee = committee
        return self

    def with_max_iterations(self, max_iterations: int):
        # for some reason reads as a string so need to cast it
        self.max_iterations = int(max_iterations)
        return self

    def with_verbose(self, verbose: bool):
        self.verbose = (int(verbose) == 1)
        return self

    def build(self):
        if self.alg is None or self.pattern == ""
        or self.committee == "" or self.max_iterations == 0:
            return None

        if len(self.committee) % len(self.pattern) != 0:
            return None
        else:
            multiplier = int(len(self.committee) / len(self.pattern))
            self.expected_output = self.pattern * multiplier

        return configuration(self.alg, self.pattern, self.committee,
                             self.expected_output,
                             self.max_iterations,
                             self.window_size, self.verbose)
