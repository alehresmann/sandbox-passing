import sys
import logging
import time

from bitarray import bitarray
from colorama import Fore

from circular_list import node, circular_list
from robot import robot
from analyser import analyser

colours = [ Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN ]

class configuration:
    def __init__(self, pattern: str, input_string: str, pf=False):
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
        self.initial_configuration = bitarray(input_string)
        self.a = analyser()
        self.pf = pf
        self.rounds_info = False

    def __len__(self):
        return len(self.configuration)

    def __str__(self):
        if self.pf:
            return self.print_full()
        else:
            return self.print_minimal()

    def print_full(self):
        node = self.configuration.first_node
        ret = ''
        for i in range(0, len(self)):
            if node.owned_by is None:
                ret += Fore.WHITE
            else:
                ret += colours[node.owned_by.ID % len(colours)]
            ret += str(int(node.data is True))
            node = node.next
        ret += Fore.WHITE
        return ret

    def print_minimal(self):
        c_string = str(self.configuration)
        pz = self.pattern.count(False)

        slice_ownership = []
        node = self.configuration.first_node
        for i in range(0, int(len(c_string) / self.slice_size)):
            if node.owned_by is None:
                slice_ownership.append(-1)
            else:
                slice_ownership.append(node.owned_by.ID)
            for j in range(0, self.slice_size):
                node = node.next

        slices = [c_string[i: i + self.slice_size] for i in range(0, len(c_string), self.slice_size)]

        heaviness = []
        for s in slices:
            if s.count('0') - pz == 0:
                if s == self.pattern.to01():
                    heaviness.append('P')
                else:
                    heaviness.append('V')
            else:
                heaviness.append(int(bool(s.count('0') < pz)))

        ret = ''
        for i, z in enumerate(heaviness):
            if slice_ownership[i] == -1:
                ret += Fore.WHITE
            else:
                ret += colours[slice_ownership[i] % len(colours)]
            ret += str(z) + ' '
        ret += Fore.WHITE
        return ret

    def get_robots_stats(self):
        ret = Fore.WHITE + 'STATS:\n'
        for bot in self.bots:
            ret += colours[bot.ID % len(colours)] + bot.get_stats() + '\n'
        ret += Fore.WHITE
        return ret

    def get_config_stats(self):
        return str(self.a.get_upper_bound(self.initial_configuration.to01(), self.pattern.to01()))

    def get_round_stats(self):
        return 'i: ' + str(self.a.count_invalid(str(self.configuration), self.pattern.to01()))

    def attach_bot(self, index: int):
        check = self.configuration.get_node_at(index)
        for i in range(0, self.slice_size * 2):
            if check.owned_by is not None:
                raise AssertionError('Can\'t place bot at ' +str(index) +'! Overlapping with R'+ str(check.owned_by))
            check = check.next

        temp = self.configuration.get_node_at(index)

        bot = robot(len(self.bots), self.pattern, temp, self.k)
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
            if bot.state:
                return False
        return True

    def run_round(self):
        for bot in self.bots:

            if len(bot.commands) == 0:
                bot.algo_round()

            for i in range(0, len(bot.commands)):
                com = bot.commands.pop(0)
                com.execute()
            logging.debug(bot)

    def run_algo(self, max_iterations: int):
        round_count = 1
        logging.debug('\n')
        extra = ''
        while round_count < max_iterations:
            if self.rounds_info:
                extra = self.get_round_stats()
            logging.info('\nRound ' + str(round_count) + ' start:\t' + str(self) + ' ' + extra)
            self.run_round()
            round_count += 1
            logging.debug('\n')
            if self.all_done():
                logging.info('\nEND: \t\t' + str(self) + ' ' + extra)
                break

        if self.check_if_patterned():

            #if self.a.get_upper_bound(self.initial_configuration.to01(), self.pattern.to01()) < self.bots[0].total_rounds:
            #        print(self.initial_configuration.to01(),
            #                self.a.get_upper_bound(self.initial_configuration.to01(), self.pattern.to01()),
            #                self.bots[0].total_rounds, self.a.get_upper_bound(self.initial_configuration.to01(), self.pattern.to01()) - self.bots[0].total_rounds)
            #if self.bots[0].total_rounds >= 130:
            #    print(self.initial_configuration.to01())
            logging.warning('\nSUCCESS!')
            logging.warning('total rounds:' + str(self.bots[0].total_rounds))

        else:
            logging.warning(self.get_robots_stats())
            raise ValueError('ERROR! did I run out of rounds or claim  to be done when I wasn\'t?')
            logging.warning(self.configuration)
