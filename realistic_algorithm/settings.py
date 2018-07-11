import sys
import logging

from bitarray import bitarray

from robot import robot


class settings:
    def __init__(self, inpt: bitarray, pattern: bitarray, max_iterations=10000):
        # minor exception handling
        if len(inpt) % len(pattern) != 0:
            print('invalid pattern length!')
            sys.exit(0)

        # settings
        self.inpt = inpt
        self.pattern = pattern
        self.robot_count = int(len(inpt) / (len(pattern) * 2))
        self.max_iterations = max_iterations

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
            self.robots.append(robot(self.pattern, window, sandbox, robot_count, int(len(windows)/2)))
            robot_count += 1

    def all_are_done(self):
        for bot in self.robots:
            if bot.done == False:
                return False
        return True

    def print_robots(self):
        ret = str(self.iteration_count) + ':'
        for bot in self.robots:
            ret += ' ' + str(bot)
        return ret

    def preliminary(self):
        logging.debug('starting position:')
        logging.debug(self.print_robots())

        logging.debug('applying preliminary step')
        for bot in self.robots:
            bot.preliminary()
        logging.debug(self.print_robots())

    def algorithm(self):
        self.preliminary()

        logging.debug('beginning algorithm')
        print(self.all_are_done())
        while not self.all_are_done() and self.iteration_count < self.max_iterations:
            self.iteration_count += 1

            logging.debug('verifying validity of entire string')
            #for bot in self.robots:
            #    if bot.consecutive_valid_sandboxes > bot.num_of_other_bots:
            #        #bot.reach_pattern()
            #        bot.done = True

            logging.debug('moving things locally:')
            for bot in self.robots:
                    if bot.has_valid_sandbox():
                        bot.consecutive_valid_sandboxes += 1
                    else:
                        bot.consecutive_valid_sandboxes = 0
                        if not bot.has_valid_window():
                            bot.rearrange_from_sandbox()
            logging.debug(self.print_robots())

            logging.debug('swapping sandbox and window locally if needed:')
            for bot in self.robots:
                if bot.done or bot.is_satisfied:
                    continue
                elif bot.consecutive_valid_sandboxes == bot.num_of_other_bots:
                    if bot.window_zero_count > bot.pattern_zero_count:
                        # someone else is stuck with my 1s. I expulse my window and how they will catch it.
                        bot.swap()
                elif bot.window_zero_count == bot.pattern_zero_count and bot.sandbox_zero_count != bot.pattern_zero_count:
                    bot.swap()
            logging.debug(self.print_robots())

            logging.debug('trading sandboxes:')
            for bot in self.robots:
                self.robots[0].trade_sandbox_with(bot)
            logging.debug(self.print_robots())

            valid = True
            for rob in self.robots:
                if rob.window.count() != rob.pattern.count() or rob.sandbox.count() != rob.pattern.count():
                    valid = False
            if valid:
                return True

        #if self.iteration_count == self.max_iterations:
        #    return False
        #logging.info('reached pattern.')
        logging.info('FINISHED: ' + self.print_robots())
        logging.debug('VERIFYING...')
        for rob in self.robots:
            if rob.window.count() != rob.pattern.count() or rob.sandbox.count() != rob.pattern.count():
                return False
        logging.info('num of iterations: ' + str(self.iteration_count) + '\ninput string of length ' + str(len(self.inpt)) + '\n' + str(len(self.robots)) + ' robots with windows of size ' + str(len(self.robots[0].window)) + '\n\n')
        return True
