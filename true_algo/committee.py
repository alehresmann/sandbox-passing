import sys
import logging

from bitarray import bitarray
from circular_list import node, circular_list
from robot import robot

class configuration:
    def __init__(self, pattern: str, input_string: str, max_iterations: int):
        self.pattern = bitarray(pattern)
        self.slice_size = len(pattern)
        self.configuration = circular_list(input_string)
        self.max_iterations = max_iterations
        self.bots = []

    def __len__(self):
        return len(self.configuration)

    def __str__(self):
        return str(self.configuration)

    def attach_bot(self, index: int, ID: int):
        check = self.configuration.get_node_at(index)
        for i in range(0, self.slice_size * 2):
            if check.owned_by is not None:
                logging.warning('Can\'t place bot here! Overlapping with R'+ str(check.owned_by))
                return
            check = check.next

        temp = self.configuration.get_node_at(index)

        bot = robot(len(self.bots), self.pattern, temp, int(len(self.configuration) / self.slice_size))
        for i in range(0, self.slice_size * 2):
            temp.owned_by = bot
            temp = temp.next
        self.bots.append(bot)

    def run_algo(self):
        for i in range(0, self.max_iterations):
            self.run_iteration()
            logging.info(self)
            if all([bot.state == 2 for bot in self.bots]):
                logging.warning('VALID!')
                return
        logging.warning('ran out of iterations...')
        return

    def run_iteration(self):
        for bot in self.bots:
            if len(bot.commands) == 0:
                bot.algo_iter()
            done_one_op = False
            while not done_one_op:
                if len(bot.commands) > 0:
                    com = bot.commands.pop(0)
                    com.execute()
                    done_one_op = com.count_as_op
                else:
                    done_one_op = True
            logging.debug(bot)
