import sys
import logging
import time

from bitarray import bitarray
from colorama import Fore

from circular_list import node, circular_list
from robot import robot

class configuration:
    def __init__(self, pattern: str, input_string: str):
        self.pattern = bitarray(pattern)
        self.slice_size = len(pattern)
        self.configuration = circular_list(input_string)
        self.bots = []

    def __len__(self):
        return len(self.configuration)

    def __str__(self):
        return str(self.configuration)

    def attach_bot(self, index: int, is_synchronised=False):
        check = self.configuration.get_node_at(index)
        for i in range(0, self.slice_size * 2):
            if check.owned_by is not None:
                raise ValueError('Can\'t place bot at ' +str(index) +'! Overlapping with R'+ str(check.owned_by))
            check = check.next

        temp = self.configuration.get_node_at(index)

        bot = robot(len(self.bots), self.pattern, temp, int(len(self.configuration) / self.slice_size), is_synchronised)
        for i in range(0, self.slice_size * 2):
            temp.owned_by = bot
            temp = temp.next
        self.bots.append(bot)

    def check_validity(self):
        current = self.configuration.first_node
        count = 0
        while count < len(self):
            if current.data != self.pattern[count % len(self.pattern)]:
                print('problem at ' + str(count))
                return False
            current = current.next
            count += 1
        return True

    def all_done(self):
        for bot in self.bots:
            if bot.state < 2:
                return False
        return True

    def print_robots_final(self):
        colours = [ Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN ]
        logging.warning(Fore.WHITE + 'STATS:')
        for bot in self.bots:
            logging.warning(colours[bot.ID % len(colours)] + bot.final_state())
        logging.warning(Fore.WHITE)

    def run_algo(self, max_iterations: int):
        logging.info(self)
        tick_count = 0
        while tick_count < max_iterations:
            self.run_iteration()
            logging.info(self)
            if self.all_done():
                break
            tick_count += 1

        if self.check_validity():
            print('\nVALID!')
        else:
            raise ValueError('ERROR! did I run out of rounds or claim  to be done when I wasn\'t?')

    def run_synchronised_algo(self, max_iterations: int):
        logging.info(self)
        tick_count = 0
        while tick_count < max_iterations:
            self.run_synchronised_round()
            logging.info(self)
            if self.all_done():
                break
            tick_count += 1

        if self.check_validity():
            print('\nVALID!')
        else:
            self.print_robots_final()
            raise ValueError('ERROR! did I run out of rounds or claim  to be done when I wasn\'t?')

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

    def run_synchronised_round(self):
        for bot in self.bots:
            done_move = False
            while not done_move:
                if len(bot.commands) == 0:
                    bot.algo_iter()
                if len(bot.commands) > 0:
                    if len(bot.commands) > 1 and str(bot.commands[-2]) == 'move':
                        done_move = True
                    for i in range(0, len(bot.commands)):
                        com = bot.commands.pop(0)
                        com.execute()

                else:
                    done_move = True
                logging.debug(bot)

