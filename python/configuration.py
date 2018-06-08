import sys
from algo import algo
from committee import committee

class configuration:
    def __init__(self, alg: algo, c: committee, max_iterations: int, verbose: bool, no_cycles: bool):
        self.alg = alg
        self.c = c
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.no_cycles = no_cycles

class configuration_builder:
    def __init__(self):
        self.alg = None
        self.c = None
        self.max_iterations = 0
        self.verbose = False

    def with_alg(self, alg: algo):
        self.alg = alg
        return self

    def with_pattern(self, pattern: str):
        self.pattern = pattern
        return self

    def with_committee(self, c: committee):
        self.c = c
        return self

    def with_max_iterations(self, max_iterations: int):
        self.max_iterations = max_iterations
        return self

    def with_verbose(self, verbose: bool):
        self.verbose = verbose
        return self

    def with_no_cycles(self, no_cycles: bool):
        self.no_cycles = no_cycles
        return self

    def build(self):
        if self.alg is None or self.c is None or self.max_iterations == 0:
            return None

        return configuration(self.alg, self.c,
                             self.max_iterations, self.verbose, self.no_cycles)
