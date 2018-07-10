import sys
import logging

from bitarray import bitarray

from patterned_robot import robot


class settings:
    def __init__(self, inpt: bitarray, pattern: bitarray, max_iteration=10000):
        # minor exception handling
        if len(inpt) % len(pattern) != 0:
            print('invalid pattern length!')
            sys.exit(0)

        # settings
        self.inpt = inpt
        self.pattern = pattern
        self.robot_count = int(len(inpt) / (len(pattern) * 2))
        self.max_iteration = max_iteration
        # vars necessary for running the algo itself
        self.robots = []
        self.iteration_count = 0

    def _pairwise(self, it):
        it = iter(it)
        while True:
            yield next(it), next(it)

    def _split_bitarray(self, arr: bitarray, partition_length: int):
        l = []
        for i in range(0, len(arr), partition_length):
            l.append(arr[i: i + partition_length])
        return l

    def assign_windows_to_robots(self):
        windows = self._split_bitarray(self.inpt, len(self.pattern))
        robot_count = 0
        for window, sandbox in self._pairwise(windows):
            robot_count += 1
            self.robots.append(robot(self.pattern, window, sandbox, robot_count))

    def is_patterned(self):
        for rob in self.robots:
            if not rob.window == self.pattern or not rob.sandbox == self.pattern:
                return False
        return True

    def print_robots(self):
        ret = str(self.iteration_count) + ':'
        for rob in self.robots:
            ret += ' ' + str(rob)
        return ret

    def preliminary_step(self):
        logging.info('Preliminary step: rearranging window, sorting sandbox.')
        for rob in self.robots:
            rob.rearrange_window()
            rob.sandbox.sort()

    def algorithm(self):
        self.preliminary_step()

        logging.info('starting...')
        while not self.is_patterned() and self.iteration_count < self.max_iteration:
            self.iteration_count += 1
            logging.debug(self.print_robots())

            logging.debug('rearranging from sandbox unless sandbox is pattern...')
            for rob in self.robots:
                if not rob.has_valid_sandbox() and not rob.has_valid_window():
                    rob.sandbox.sort()
                    rob.rearrange_from_sandbox()
                if not rob.has_valid_window():
                    rob.expulse_window()
            logging.debug(self.print_robots())

            logging.debug('swapping sandboxes and windows if needed...')
            for rob in self.robots:
                if rob.dont_swap:
                    rob.dont_swap = False
                    break
                if rob.has_valid_window() and not rob.has_valid_sandbox():
                    rob.rearrange_sandbox()
                    rob.swap()

            logging.debug(self.print_robots())

            logging.debug('passing sandboxes...')
            for rob in self.robots:
                self.robots[0].trade_sandboxes_with(rob)
            logging.debug(self.print_robots())
        logging.debug(self.print_robots())
        if self.iteration_count == self.max_iteration:
            return False
        return True

