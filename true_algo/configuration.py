import sys
import logging
import time

from bitarray import bitarray
from colorama import Fore

from circular_list import node, circular_list
from robot import robot

colours = [ Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN ]

class configuration:
    def __init__(self, pattern: str, input_string: str):
        try:
            int(pattern, 2)
            int(input_string, 2)
        except:
            raise AssertionError('You didn\'t give me binary strings for your pattern and/or your configuration!')

        if not len(input_string) % len(pattern) == 0:
            raise AssertionError('Your input_string\'s length doesn\'t divide perfectly in your pattern\'s length!')

        self.k = int(len(input_string) / len(pattern))

        if not pattern.count('0') == int(input_string.count('0') / self.k):
            raise AssertionError('Assure yourself you have the correct number of 1s and 0s in your config to reach the pattern!')

        self.configuration = circular_list(input_string)
        self.pattern = bitarray(pattern)
        self.slice_size = len(pattern)
        self.bots = []

    def __len__(self):
        return len(self.configuration)

    def __str__(self):
        return str(self.configuration)

    def attach_bot(self, index: int, is_synchronised=False):
        check = self.configuration.get_node_at(index)
        for i in range(0, self.slice_size * 2):
            if check.owned_by is not None:
                raise AssertionError('Can\'t place bot at ' +str(index) +'! Overlapping with R'+ str(check.owned_by))
            check = check.next

        temp = self.configuration.get_node_at(index)

        bot = robot(len(self.bots), self.pattern, temp, self.k, is_synchronised)
        for i in range(0, self.slice_size * 2):
            temp.owned_by = bot
            temp = temp.next
        self.bots.append(bot)

    def check_if_patterned(self):
        current = self.configuration.first_node
        count = 0
        while count < len(self):
            if current.data != self.pattern[count % len(self.pattern)]:
                logging.warning('problem at ' + str(count))
                return False
            current = current.next
            count += 1
        return True

    def all_done(self):
        for bot in self.bots:
            if bot.state < 2:
                return False
        return True

    def get_robots_final(self):
        ret = Fore.WHITE + 'STATS:\n'
        for bot in self.bots:
            ret += colours[bot.ID % len(colours)] + bot.final_state() + '\n'
        ret += Fore.WHITE
        return ret

    def run_round(self, synchronised):
        for bot in self.bots:

            if len(bot.commands) == 0:
                bot.algo_round()

            for i in range(0, len(bot.commands)):
                com = bot.commands.pop(0)
                com.execute()
                if not synchronised and com.count_as_op:
                    break
            logging.debug(bot)

    def run_algo(self, max_iterations: int, synchronise=False):
        round_count = 1
        logging.info('Round ' + str(round_count) + ':\t ' + str(self))
        logging.debug('\n')
        while round_count < max_iterations:
            self.run_round(synchronise)
            round_count += 1
            logging.info('Round ' + str(round_count) + ':\t ' + str(self))
            logging.debug('\n')
            if self.all_done():
                break

        if self.check_if_patterned():
            logging.warning('\nSUCCESS!')
        else:
            logging.warning(self.get_robots_final())
            raise ValueError('ERROR! did I run out of rounds or claim  to be done when I wasn\'t?')
            logging.warning(self.configuration)
