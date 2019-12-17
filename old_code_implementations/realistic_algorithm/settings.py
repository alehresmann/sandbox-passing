import sys
import logging

from bitarray import bitarray

from robot import robot


class settings:
    def __init__(self, inpt: bitarray, pattern: bitarray, max_iterations=10000):
        # minor exception handling
        if len(inpt) % (len(pattern)*2) != 0:
            print('invalid pattern length! you need the following to be true: (length of input) mod (length of pattern) = 0')
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
        ret = str(self.iteration_count) + ':\n'
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
        while not self.all_are_done() and self.iteration_count < self.max_iterations:
            self.iteration_count += 1

            logging.debug('verifying validity of entire string')
            for bot in self.robots:
                if  bot.satisfaction_array.all():  # if all bits in the array are 1
                    bot.reach_pattern()  # reorganise local window and sandbox into pattern
                    bot.done = True

            logging.debug('moving things locally:')
            for bot in self.robots:
                    if not bot.has_valid_sandbox():
                        if not bot.has_valid_window():
                            bot.rearrange_from_sandbox()
            logging.debug(self.print_robots())

            logging.debug('swapping sandbox and window locally if needed:')
            for bot in self.robots:
                if bot.has_valid_sandbox():
                    if bot.window_zero_count > bot.pattern_zero_count:
                        # someone else is stuck with my 1s. I expulse my window
                        # and hope they will catch it.
                        bot.swap()
                elif bot.window_zero_count == bot.pattern_zero_count \
                and bot.sandbox_zero_count != bot.pattern_zero_count:
                    # my window is satisfied, but my sandbox is not. swap both and
                    # wait to receive an invalid sandbox that I may take from
                    bot.swap()
            logging.debug(self.print_robots())

            logging.debug('trading sandboxes:')
            for bot in self.robots:
                self.robots[0].trade_sandbox_with(bot)
            logging.debug(self.print_robots())

            logging.debug('passing around satisfaction array')
            for i in range(0, len(self.robots) - 1):
                self.robots[i].send_satisfaction_array(self.robots[i+1])
            self.robots[-1].send_satisfaction_array(self.robots[0])

            # This isn't actually in the distributed algorithm, this is merely to end the computation once all 'robots' report being done
            valid = True
            for bot in self.robots:
                if not bot.done:
                    valid = False
            if valid:
                break

        logging.info('FINISHED: iteration ' + str(self.iteration_count))
        for bot in self.robots:
            logging.info(str(bot.ID) + ':\t' + str(bot))
        logging.debug('VERIFYING...')
        for bot in self.robots:
            if bot.window != bot.pattern or bot.sandbox != bot.pattern:
                print('ERROR AT ' + str(bot.ID))
                return False
        print('num of iterations: ' + str(self.iteration_count)) #+ '\ninput string of length ' + str(len(self.inpt)) + '\n' + str(len(self.robots)) + ' robots with windows of size ' + str(len(self.robots[0].window)) + '\n\n')
        return True
