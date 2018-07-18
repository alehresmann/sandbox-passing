import sys
import logging
import operator

from bitarray import bitarray

from robot import robot

class committee:
    def __init__(self, configuration: bitarray, pattern :bitarray, max_iterations: int):
        if len(configuration) % len(pattern) != 0:
            print('input string doesn\'t perfectly divide into pattern!')
            sys.exit(0)
        self.configuration = configuration
        self.pattern = pattern
        self.max_iterations = max_iterations
        self.bots = []
        self.iteration_count = 0

    def _insert(self, string: str, substring:str, i: int):
        return string[0:i] + substring + string[i:]

    def __str__(self):
        temp = sorted(self.bots, key=operator.attrgetter('a'))
        config_str = self.configuration.to01()
        robot_str = ' ' * len(self.configuration) + (' ' * 4 * len(temp))
        robot_offset = 0

        for bot in temp:
            config_str = self._insert(config_str, '│', bot.a + robot_offset)
            config_str = self._insert(config_str, ':', bot.a + bot.window_size + 1 + robot_offset)
            if bot.b < bot.a:
                config_str = self._insert(config_str, '│', bot.b)
            else:
                config_str = self._insert(config_str, '│', bot.b + 2 + robot_offset)

            robot_str = robot_str[:bot.a + robot_offset] + robot_str[(bot.a+1) + robot_offset:]
            robot_str = self._insert(robot_str, '└', bot.a + robot_offset)

            robot_str = robot_str[:bot.a + bot.window_size + 1] + robot_str[(bot.a+bot.window_size  + 1):]
            robot_str = self._insert(robot_str, str(bot.ID), bot.a + bot.window_size + 1 + robot_offset)

#            robot_str = robot_str[:bot.b + robot_offset] + robot_str[(bot.b+2 + robot_offset):]
            if bot.b < bot.a:
                robot_str = self._insert(robot_str, '┘', bot.b)
            else:
                robot_str = self._insert(robot_str, '┘', bot.b + 2 + robot_offset)
            robot_offset += 3
        return config_str + '\n' + robot_str

    def attach_new_bot(self, a: int, b: int):
        bot = robot(len(self.bots), self.pattern, a, b, self.configuration)
        self.bots.append(bot)

    def all_are_done(self):
        for bot in self.bots:
            if bot.done == 0:
                return False
        return True

    def algorithm(self):
        logging.debug('beginning algorithm')
        logging.debug(str(self))
        while not self.all_are_done() and self.iteration_count < self.max_iterations:
            logging.debug(str(self.iteration_count) + ':')
            self.iteration_count += 1

            logging.debug('computing')
            for bot in self.bots:
                bot.algo_iter()
            logging.debug(str(self))

            logging.debug('moving')
            for bot in self.bots:
                bot.move_by_window_size()
            logging.debug(str(self))

        logging.info('num of iterations: ' + str(self.iteration_count) + '\ninput string of length: ' + str(len(self.configuration)) + '\n' + str(len(self.bots)) + ' robots\npattern: ' + self.pattern.to01())
        logging.debug('VERIFYING...')
        substrs = [self.configuration[i:i+len(self.pattern)] for i in range(0, len(self.configuration), len(self.pattern))]
        for i, sub in enumerate(substrs):
            if sub != self.pattern:
                print('ERROR AT ' + str(i))
                return False
        print('VALID!')
        return True
